import os
from urllib.error import URLError
import numpy as np
from pathlib import Path
from typing import Callable, Optional, Union
import pandas as pd
import lightning as L
from torch.utils.data import Dataset, random_split, DataLoader
import torch

from torchvision.datasets.utils import check_integrity, download_and_extract_archive


class BiasCorrection(Dataset):
    """
    Bias Correction Dataset.

    This class provides access to a dataset used for bias correction of numerical prediction models,
    specifically for temperature forecasts. The dataset is stored in CSV format and can be optionally
    transformed using a provided function. The class includes methods for downloading, loading, and
    accessing the dataset, as well as applying transformations.

    Args:
        root (str or pathlib.Path): Root directory of the dataset where the 'BiasCorrection/Bias_correction_ucl.csv' file is located.
        download (bool, optional): If True, the dataset will be downloaded from the internet and saved to the root directory. 
                                   If the dataset already exists, it will not be downloaded again. Default is False.
        transform (callable, optional): A function/transform that takes a Pandas DataFrame and returns a transformed version.
                                        This allows for data preprocessing before it is loaded. Default is None.

    Acknowledgement:
        This class was developed with inspiration from the MNIST dataset class in torchvision.
    """

    mirrors = [
        "https://archive.ics.uci.edu/static/public/514/",
    ]

    resources = [
        (
            "bias+correction+of+numerical+prediction+model+temperature+forecast.zip",
            "3deee56d461a2686887c4ae38fe3ccf3",
        ),
    ]

    def __init__(
        self,
        root: Union[str, Path],
        download: bool = False,
        transform: Optional[Callable] = None,
    ) -> None:
        """
        Initializes the BiasCorrection dataset, optionally downloading it if necessary.

        Args:
            root (Union[str, Path]): The root directory where the dataset will be stored or accessed.
            download (bool, optional): If True, downloads the dataset from the provided mirrors. Default is False.
            transform (Optional[Callable], optional): A function to transform the data before loading. Default is None.
        """

        super().__init__()
        self.root = root
        self.transform = transform

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError(
                "Dataset not found. You can use download=True to download it"
            )

        self.data_input, self.data_output = self._load_data()

    def _load_data(self):
        """
        Loads the dataset from the CSV file, applies transformations (if provided), and separates the data into input and output variables.

        Returns:
            Tuple: A tuple containing two numpy arrays: `data_input` (input data) and `data_output` (output data).
        """

        if self.transform:
            data: pd.DataFrame = (
                pd.read_csv(os.path.join(self.data_folder, "Bias_correction_ucl.csv"))
                .pipe(self.transform)
                .pipe(self.add_input_output_temperature)
            )
        else:
            data: pd.DataFrame = pd.read_csv(
                os.path.join(self.data_folder, "Bias_correction_ucl.csv")
            ).pipe(self.add_input_output_temperature)

        data_input = data["Input"].to_numpy(dtype=np.float32)
        data_output = data["Output"].to_numpy(dtype=np.float32)

        return data_input, data_output

    def __len__(self):
        """
        Returns the number of examples in the dataset.

        Returns:
            int: The total number of examples in the dataset (i.e., the number of rows in the input data).
        """
        
        return self.data_input.shape[0]

    def __getitem__(self, idx):
        """
        Retrieves a single example and its corresponding target from the dataset.

        Args:
            idx (int): The index of the example to retrieve.

        Returns:
            Tuple: A tuple containing two tensors: the input example and the target output.
        """

        example = self.data_input[idx, :]
        target = self.data_output[idx, :]
        example = torch.tensor(example)
        target = torch.tensor(target)
        return example, target

    @property
    def data_folder(self) -> str:
        """
        Returns the path to the folder where the dataset is stored.

        Returns:
            str: The path to the dataset folder within the root directory.
        """

        return os.path.join(self.root, self.__class__.__name__)

    def _check_exists(self) -> bool:
        """
        Checks if the dataset files exist and their integrity is verified.

        Returns:
            bool: True if the dataset exists and is valid, otherwise False.
        """

        return all(
            check_integrity(os.path.join(self.data_folder, file_path), checksum)
            for file_path, checksum in self.resources
        )

    def download(self) -> None:
        """
        Downloads the dataset from the provided mirrors and extracts it.

        The method ensures the dataset is downloaded and extracted to the appropriate folder. 
        If the dataset is already present, it will not be downloaded again.
        """

        if self._check_exists():
            return

        os.makedirs(self.data_folder, exist_ok=True)

        # download files
        for filename, md5 in self.resources:
            errors = []
            for mirror in self.mirrors:
                url = f"{mirror}{filename}"
                try:
                    download_and_extract_archive(
                        url, download_root=self.data_folder, filename=filename, md5=md5
                    )
                except URLError as e:
                    errors.append(e)
                    continue
                break
            else:
                s = f"Error downloading {filename}:\n"
                for mirror, err in zip(self.mirrors, errors):
                    s += f"Tried {mirror}, got:\n{str(err)}\n"
                raise RuntimeError(s)

    @staticmethod
    def add_input_output_temperature(df: pd.DataFrame) -> pd.DataFrame:
        """Add a multiindex denoting if the column is an input or output variable."""
        # copy the dataframe
        temp_df = df.copy()
        # extract all the column names
        column_names = temp_df.columns.tolist()
        # only the last 2 columns are output variables, all others are input variables. So make list of corresponding lengths of 'Input' and 'Output'
        input_list = ["Input"] * (len(column_names) - 2)
        output_list = ["Output"] * 2
        # concat both lists
        input_output_list = input_list + output_list
        # define multi index for attaching this 'Input' and 'Output' list with the column names already existing
        multiindex_bias = pd.MultiIndex.from_arrays([input_output_list, column_names])
        # transpose such that index can be adjusted to multi index
        new_df = pd.DataFrame(df.transpose().to_numpy(), index=multiindex_bias)
        # transpose back such that columns are the same as before except with different labels
        return new_df.transpose()


class BCDataModule(L.LightningDataModule):
    """Bias Correction dataset module."""

    def __init__(
        self,
        dataset_directory: str = "./datasets",
        batch_size: int = 32,
        train_size: float = 0.8,
        val_size: float = 0.1,
        test_size: float = 0.1,
        shuffle_train: bool = True,
        shuffle_val: bool = False,
        shuffle_test: bool = False,
        num_workers: int = 4,
        pin_memory: bool = False,
    ) -> None:
        super().__init__()
        # Define required parameters here
        self.batch_size = batch_size
        self.dataset_directory = dataset_directory
        self.train_size = train_size
        self.val_size = val_size
        self.test_size = test_size
        self.shuffle_train = shuffle_train
        self.shuffle_val = shuffle_val
        self.shuffle_test = shuffle_test
        self.num_workers = num_workers
        self.pin_memory = pin_memory

    def prepare_data(self):
        # Define steps that should be done
        # on only one GPU, like getting data.
        BiasCorrection(self.dataset_directory, download=True, transform=self.transform)

    def setup(self, stage=None):
        # Define steps that should be done on
        # every GPU, like splitting data, applying
        # transform etc.
        data = BiasCorrection(self.dataset_directory, transform=self.transform)

        train_val_data, self.test_data = random_split(
            data, [1 - self.test_size, self.test_size]
        )
        self.train_data, self.val_data = random_split(
            train_val_data,
            [
                self.train_size / (1 - self.test_size),
                self.val_size / (1 - self.test_size),
            ],
        )

    def train_dataloader(self):
        # Return DataLoader for Training Data here
        return DataLoader(
            self.train_data,
            batch_size=self.batch_size,
            shuffle=self.shuffle_train,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

    def val_dataloader(self):
        # Return DataLoader for Validation Data here
        return DataLoader(
            self.val_data,
            batch_size=self.batch_size,
            shuffle=self.shuffle_val,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

    def test_dataloader(self):
        # Return DataLoader for Testing Data here
        return DataLoader(
            self.test_data,
            batch_size=self.batch_size,
            shuffle=self.shuffle_test,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

    @staticmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        def date_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
            """Transform the string that denotes the date to the datetime format in pandas."""
            # make copy of dataframe
            df_temp = df.copy()
            # add new column at the front where the date string is transformed to the datetime format
            df_temp.insert(0, "DateTransformed", pd.to_datetime(df_temp["Date"]))
            return df_temp

        def add_year(df: pd.DataFrame) -> pd.DataFrame:
            """Extract the year from the datetime cell and add it as a new column to the dataframe at the front."""
            # make copy of dataframe
            df_temp = df.copy()
            # extract year and add new column at the front containing these numbers
            df_temp.insert(0, "Year", df_temp["DateTransformed"].dt.year)
            return df_temp

        def add_month(df: pd.DataFrame) -> pd.DataFrame:
            """Extract the month from the datetime cell and add it as a new column to the dataframe at the front."""
            # make copy of dataframe
            df_temp = df.copy()
            # extract month and add new column at index 1 containing these numbers
            df_temp.insert(1, "Month", df_temp["DateTransformed"].dt.month)
            return df_temp

        def add_day(df: pd.DataFrame) -> pd.DataFrame:
            """Extract the day from the datetime cell and add it as a new column to the dataframe at the front."""
            # make copy of dataframe
            df_temp = df.copy()
            # extract day and add new column at index 2 containing these numbers
            df_temp.insert(2, "Day", df_temp["DateTransformed"].dt.day)
            return df_temp

        def normalize_columns_bias(df: pd.DataFrame) -> pd.DataFrame:
            """Normalize the columns for the bias correction dataset. This is different from normalizing all the columns separately because the
            upper and lower bounds for the output variables are assumed to be the same.
            """
            # copy the dataframe
            temp_df = df.copy()
            # normalize each column
            for feature_name in df.columns:
                # the output columns are normalized using the same upper and lower bound for more efficient check of the inequality
                if feature_name == "Next_Tmax" or feature_name == "Next_Tmin":
                    max_value = 38.9
                    min_value = 11.3
                # the input columns are normalized using their respective upper and lower bounds
                else:
                    max_value = df[feature_name].max()
                    min_value = df[feature_name].min()
                temp_df[feature_name] = (df[feature_name] - min_value) / (
                    max_value - min_value
                )
            return temp_df

        def sample_2500_examples(df: pd.DataFrame) -> pd.DataFrame:
            """Sample 2500 examples from the dataframe without replacement."""
            temp_df = df.copy()
            sample_df = temp_df.sample(n=2500, replace=False, random_state=3, axis=0)
            return sample_df

        return (
            # drop missing values
            df.dropna(how="any")
            # transform string date to datetime format
            .pipe(date_to_datetime)
            # add year as a single column
            .pipe(add_year)
            # add month as a single column
            .pipe(add_month)
            # add day as a single column
            .pipe(add_day)
            # remove original date string and the datetime format
            .drop(["Date", "DateTransformed"], axis=1, inplace=False)
            # convert all numbers to float32
            .astype("float32")
            # normalize columns
            .pipe(normalize_columns_bias)
            # sample 2500 examples out of the dataset
            .pipe(sample_2500_examples)
        )


class FiniteIncome(Dataset):
    """Finite Income Dataset.

    Args:
        root (str or ``pathlib.Path``): Root directory of dataset where ``BiasCorrection/Bias_correction_ucl.csv`` exists.
        download (bool, optional): If True, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
        transform (callable, optional): A function/transform that takes in a Pandas DataFrame
            and returns a transformed version.

    Acknowledgement:
        This class was developed with inspiration from the MNIST dataset class in torchvision.
    """

    mirrors = [
        "https://www.kaggle.com/api/v1/datasets/download/grosvenpaul/",
    ]

    resources = [
        (
            "family-income-and-expenditure",
            "7d74bc7facc3d7c07c4df1c1c6ac563e",
        ),
    ]

    def __init__(
        self,
        root: Union[str, Path],
        download: bool = False,
        transform: Optional[Callable] = None,
    ) -> None:
        super().__init__()
        self.root = root
        self.transform = transform

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError(
                "Dataset not found. You can use download=True to download it"
            )

        self.data_input, self.data_output = self._load_data()

    def _load_data(self):

        if self.transform:
            data: pd.DataFrame = pd.read_csv(
                os.path.join(self.data_folder, "Family Income and Expenditure.csv")
            ).pipe(self.transform)
        else:
            data: pd.DataFrame = pd.read_csv(
                os.path.join(self.data_folder, "Family Income and Expenditure.csv")
            ).pipe(self.add_input_output_family_income)

        data_input = data["Input"].to_numpy(dtype=np.float32)
        data_output = data["Output"].to_numpy(dtype=np.float32)

        return data_input, data_output

    def __len__(self):
        return self.data_input.shape[0]

    def __getitem__(self, idx):
        example = self.data_input[idx, :]
        target = self.data_output[idx, :]
        example = torch.tensor(example)
        target = torch.tensor(target)
        return example, target

    @property
    def data_folder(self) -> str:
        return os.path.join(self.root, self.__class__.__name__)

    def _check_exists(self) -> bool:
        return all(
            check_integrity(os.path.join(self.data_folder, file_path), checksum)
            for file_path, checksum in self.resources
        )

    def download(self) -> None:
        """Download the MNIST data if it doesn't exist already."""

        if self._check_exists():
            return

        os.makedirs(self.data_folder, exist_ok=True)

        # download files
        for filename, md5 in self.resources:
            errors = []
            for mirror in self.mirrors:
                url = f"{mirror}{filename}"
                try:
                    download_and_extract_archive(
                        url, download_root=self.data_folder, filename=filename, md5=md5
                    )
                except URLError as e:
                    errors.append(e)
                    continue
                break
            else:
                s = f"Error downloading {filename}:\n"
                for mirror, err in zip(self.mirrors, errors):
                    s += f"Tried {mirror}, got:\n{str(err)}\n"
                raise RuntimeError(s)

    @staticmethod
    def add_input_output_family_income(df: pd.DataFrame) -> pd.DataFrame:
        """Add a multiindex denoting if the column is an input or output variable."""
        # copy the dataframe
        temp_df = df.copy()
        # extract all the column names
        column_names = temp_df.columns.tolist()
        # the 2nd-9th columns correspond to output variables and all others to input variables. So make list of corresponding lengths of 'Input' and 'Output'
        input_list_start = ["Input"]
        input_list_end = ["Input"] * (len(column_names) - 9)
        output_list = ["Output"] * 8
        # concat both lists
        input_output_list = input_list_start + output_list + input_list_end
        # define multi index for attaching this 'Input' and 'Output' list with the column names already existing
        multiindex_bias = pd.MultiIndex.from_arrays([input_output_list, column_names])
        # transpose such that index can be adjusted to multi index
        new_df = pd.DataFrame(df.transpose().to_numpy(), index=multiindex_bias)
        # transpose back such that columns are the same as before except with different labels
        return new_df.transpose()


class FIDataModule(L.LightningDataModule):
    """Finite Income dataset module."""

    def __init__(
        self,
        dataset_directory: str = "./datasets",
        batch_size: int = 32,
        train_size: float = 0.8,
        val_size: float = 0.1,
        test_size: float = 0.1,
        shuffle_train: bool = True,
        shuffle_val: bool = False,
        shuffle_test: bool = False,
        num_workers: int = 4,
        pin_memory: bool = False,
    ) -> None:
        super().__init__()
        # Define required parameters here
        self.batch_size = batch_size
        self.dataset_directory = dataset_directory
        self.train_size = train_size
        self.val_size = val_size
        self.test_size = test_size
        self.shuffle_train = shuffle_train
        self.shuffle_val = shuffle_val
        self.shuffle_test = shuffle_test
        self.num_workers = num_workers
        self.pin_memory = pin_memory

    def prepare_data(self):
        # Define steps that should be done
        # on only one GPU, like getting data.
        # TODO downloading currently disabled since not compatible with api
        # FiniteIncome(self.dataset_directory, download=True, transform=self.transform)
        pass

    def setup(self, stage=None):
        # Define steps that should be done on
        # every GPU, like splitting data, applying
        # transform etc.
        data = FiniteIncome(self.dataset_directory, transform=self.transform)

        train_val_data, self.test_data = random_split(
            data, [1 - self.test_size, self.test_size]
        )
        self.train_data, self.val_data = random_split(
            train_val_data,
            [
                self.train_size / (1 - self.test_size),
                self.val_size / (1 - self.test_size),
            ],
        )

    def train_dataloader(self):
        # Return DataLoader for Training Data here
        return DataLoader(
            self.train_data,
            batch_size=self.batch_size,
            shuffle=self.shuffle_train,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

    def val_dataloader(self):
        # Return DataLoader for Validation Data here
        return DataLoader(
            self.val_data,
            batch_size=self.batch_size,
            shuffle=self.shuffle_val,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

    def test_dataloader(self):
        # Return DataLoader for Testing Data here
        return DataLoader(
            self.test_data,
            batch_size=self.batch_size,
            shuffle=self.shuffle_test,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

    @staticmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        def normalize_columns_income(df: pd.DataFrame) -> pd.DataFrame:
            """Normalize the columns for the Family Income dataframe. This can also be applied to other dataframes because this function normalizes
            all columns individually."""
            # copy the dataframe
            temp_df = df.copy()
            # normalize each column
            for feature_name in df.columns:
                max_value = df[feature_name].max()
                min_value = df[feature_name].min()
                temp_df[feature_name] = (df[feature_name] - min_value) / (
                    max_value - min_value
                )
            return temp_df

        def check_constraints_income(df: pd.DataFrame) -> pd.DataFrame:
            """Check if all the constraints are satisfied for the dataframe and remove the examples that do not satisfy the constraint. This
            function only works for the Family Income dataset and the constraints are that the household income is larger than all the expenses
            and the food expense is larger than the sum of the other (more detailed) food expenses.
            """
            temp_df = df.copy()
            # check that household income is larger than expenses in the output
            input_array = temp_df["Input"].to_numpy()
            income_array = np.add(
                np.multiply(
                    input_array[:, [0, 1]],
                    np.subtract(
                        np.asarray([11815988, 9234485]), np.asarray([11285, 0])
                    ),
                ),
                np.asarray([11285, 0]),
            )
            expense_array = temp_df["Output"].to_numpy()
            expense_array = np.add(
                np.multiply(
                    expense_array,
                    np.subtract(
                        np.asarray(
                            [
                                791848,
                                437467,
                                140992,
                                74800,
                                2188560,
                                1049275,
                                149940,
                                731000,
                            ]
                        ),
                        np.asarray([3704, 0, 0, 0, 1950, 0, 0, 0]),
                    ),
                ),
                np.asarray([3704, 0, 0, 0, 1950, 0, 0, 0]),
            )
            expense_array_without_dup = expense_array[:, [0, 4, 5, 6, 7]]
            sum_expenses = np.sum(expense_array_without_dup, axis=1)
            total_income = np.sum(income_array, axis=1)
            sanity_check_array = np.greater_equal(total_income, sum_expenses)
            temp_df["Unimportant"] = sanity_check_array.tolist()
            reduction = temp_df[temp_df.Unimportant]
            drop_reduction = reduction.drop("Unimportant", axis=1)

            # check that the food expense is larger than all the sub expenses
            expense_reduced_array = drop_reduction["Output"].to_numpy()
            expense_reduced_array = np.add(
                np.multiply(
                    expense_reduced_array,
                    np.subtract(
                        np.asarray(
                            [
                                791848,
                                437467,
                                140992,
                                74800,
                                2188560,
                                1049275,
                                149940,
                                731000,
                            ]
                        ),
                        np.asarray([3704, 0, 0, 0, 1950, 0, 0, 0]),
                    ),
                ),
                np.asarray([3704, 0, 0, 0, 1950, 0, 0, 0]),
            )
            food_mul_expense_array = expense_reduced_array[:, [1, 2, 3]]
            food_mul_expense_array_sum = np.sum(food_mul_expense_array, axis=1)
            food_expense_array = expense_reduced_array[:, 0]
            sanity_check_array = np.greater_equal(
                food_expense_array, food_mul_expense_array_sum
            )
            drop_reduction["Unimportant"] = sanity_check_array.tolist()
            new_reduction = drop_reduction[drop_reduction.Unimportant]
            satisfied_constraints_df = new_reduction.drop("Unimportant", axis=1)

            return satisfied_constraints_df

        def sample_2500_examples(df: pd.DataFrame) -> pd.DataFrame:
            """Sample 2500 examples from the dataframe without replacement."""
            temp_df = df.copy()
            sample_df = temp_df.sample(n=2500, replace=False, random_state=3, axis=0)
            return sample_df

        def add_input_output_family_income(df: pd.DataFrame) -> pd.DataFrame:
            """Add a multiindex denoting if the column is an input or output variable."""
            # copy the dataframe
            temp_df = df.copy()
            # extract all the column names
            column_names = temp_df.columns.tolist()
            # the 2nd-9th columns correspond to output variables and all others to input variables. So make list of corresponding lengths of 'Input' and 'Output'
            input_list_start = ["Input"]
            input_list_end = ["Input"] * (len(column_names) - 9)
            output_list = ["Output"] * 8
            # concat both lists
            input_output_list = input_list_start + output_list + input_list_end
            # define multi index for attaching this 'Input' and 'Output' list with the column names already existing
            multiindex_bias = pd.MultiIndex.from_arrays(
                [input_output_list, column_names]
            )
            # transpose such that index can be adjusted to multi index
            new_df = pd.DataFrame(df.transpose().to_numpy(), index=multiindex_bias)
            # transpose back such that columns are the same as before except with different labels
            return new_df.transpose()

        return (
            # drop missing values
            df.dropna(how="any")
            # convert object to fitting dtype
            .convert_dtypes()
            # remove all strings (no other dtypes are present except for integers and floats)
            .select_dtypes(exclude=["string"])
            # transform all numbers to same dtype
            .astype("float32")
            # drop column with label Agricultural Household indicator because this is not really a numerical input but rather a categorical/classification
            .drop(["Agricultural Household indicator"], axis=1, inplace=False)
            # this column is dropped because it depends on Agricultural Household indicator
            .drop(["Crop Farming and Gardening expenses"], axis=1, inplace=False)
            # use 8 output variables and 24 input variables
            .drop(
                [
                    "Total Rice Expenditure",
                    "Total Fish and  marine products Expenditure",
                    "Fruit Expenditure",
                    "Restaurant and hotels Expenditure",
                    "Alcoholic Beverages Expenditure",
                    "Tobacco Expenditure",
                    "Clothing, Footwear and Other Wear Expenditure",
                    "Imputed House Rental Value",
                    "Transportation Expenditure",
                    "Miscellaneous Goods and Services Expenditure",
                    "Special Occasions Expenditure",
                ],
                axis=1,
                inplace=False,
            )
            # add input and output labels to each column
            .pipe(add_input_output_family_income)
            # normalize all the columns
            .pipe(normalize_columns_income)
            # remove all datapoints that do not satisfy the constraints
            .pipe(check_constraints_income)
            # sample 2500 examples
            .pipe(sample_2500_examples)
        )
