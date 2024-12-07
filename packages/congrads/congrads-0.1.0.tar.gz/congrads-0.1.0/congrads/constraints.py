from abc import ABC, abstractmethod
from numbers import Number
import random
import string
from typing import Callable, Dict
from torch import Tensor, ge, gt, lt, le, zeros, FloatTensor, ones, tensor, float32
import logging
from torch.nn.functional import normalize

from .descriptor import Descriptor


class Constraint(ABC):
    """
    Abstract base class for defining constraints that can be applied during optimization in the constraint-guided gradient descent process.

    A constraint guides the optimization by evaluating the model's predictions and adjusting the loss based on certain conditions.
    Constraints can be applied to specific layers or neurons of the model, and they are scaled by a rescale factor to control the influence of the constraint on the overall loss.

    Attributes:
        descriptor (Descriptor): The descriptor object that provides a mapping of neurons to layers.
        constraint_name (str): A unique name for the constraint, which can be provided or generated automatically.
        rescale_factor (float): A factor used to scale the influence of the constraint on the overall loss.
        neuron_names (set[str]): A set of neuron names that are involved in the constraint.
        layers (set): A set of layers associated with the neurons specified in `neuron_names`.
    """

    descriptor: Descriptor = None

    def __init__(
        self,
        neuron_names: set[str],
        constraint_name: str = None,
        rescale_factor: float = 1.5,
    ) -> None:
        """
        Initializes the Constraint object with the given neuron names, constraint name, and rescale factor.

        Args:
            neuron_names (set[str]): A set of neuron names that are affected by the constraint.
            constraint_name (str, optional): A custom name for the constraint. If not provided, a random name is generated.
            rescale_factor (float, optional): A factor that scales the influence of the constraint. Defaults to 1.5.

        Raises:
            ValueError: If the descriptor has not been set or if a neuron name is not found in the descriptor.
        """

        # Init parent class
        super().__init__()

        # Init object variables
        self.rescale_factor = rescale_factor
        self.neuron_names = neuron_names

        # Perform checks
        if rescale_factor <= 1:
            logging.warning(
                f"Rescale factor for constraint {constraint_name} is <= 1. The network will favour general loss over the constraint-adjusted loss. Is this intended behaviour? Normally, the loss should always be larger than 1."
            )

        # If no constraint_name is set, generate one based on the class name and a random suffix
        if constraint_name:
            self.constraint_name = constraint_name
        else:
            random_suffix = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
            self.constraint_name = f"{self.__class__.__name__}_{random_suffix}"
            logging.warning(
                f"Name for constraint is not set. Using {self.constraint_name}."
            )

        if self.descriptor == None:
            raise ValueError(
                "The descriptor of the base Constraint class in not set. Please assign the descriptor to the general Constraint class with 'Constraint.descriptor = descriptor' before defining network-specific contraints."
            )

        if not rescale_factor > 1:
            self.rescale_factor = abs(rescale_factor) + 1.5
            logging.warning(
                f"Rescale factor for constraint {constraint_name} is < 1, adjusted value {rescale_factor} to {self.rescale_factor}."
            )
        else:
            self.rescale_factor = rescale_factor

        self.neuron_names = neuron_names

        self.run_init_descriptor()

    def run_init_descriptor(self) -> None:
        """
        Initializes the layers associated with the constraint by mapping the neuron names to their corresponding layers
        from the descriptor.

        This method populates the `layers` attribute with layers associated with the neuron names provided in the constraint.

        Raises:
            ValueError: If a neuron name is not found in the descriptor's mapping of neurons to layers.
        """

        self.layers = set()
        for neuron_name in self.neuron_names:
            if neuron_name in self.descriptor.neuron_to_layer.keys():
                self.layers.add(self.descriptor.neuron_to_layer[neuron_name])
            else:
                raise ValueError(
                    f'The neuron name {neuron_name} used with constraint {self.constraint_name} is not defined in the descriptor. Please add it to the correct layer using descriptor.add("layer", ...).'
                )

    @abstractmethod
    def check_constraint(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        """
        Abstract method to check if the constraint is satisfied based on the model's predictions.

        This method should be implemented in subclasses to define the specific logic for evaluating the constraint based on the model's predictions.

        Args:
            prediction (dict[str, Tensor]): A dictionary of model predictions, indexed by layer names.

        Returns:
            dict[str, Tensor]: A dictionary containing the satisfaction status of the constraint for each layer or neuron.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """

        raise NotImplementedError

    @abstractmethod
    def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        """
        Abstract method to calculate the direction in which the model's predictions need to be adjusted to satisfy the constraint.

        This method should be implemented in subclasses to define how to adjust the model's predictions based on the constraint.

        Args:
            prediction (dict[str, Tensor]): A dictionary of model predictions, indexed by layer names.

        Returns:
            dict[str, Tensor]: A dictionary containing the direction for each layer or neuron, to adjust the model's predictions.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError


class ScalarConstraint(Constraint):
    """
    A subclass of the `Constraint` class that applies a scalar constraint on a specific neuron in the model.

    This constraint compares the value of a specific neuron in the model to a scalar value using a specified comparator (e.g., greater than, less than).
    If the constraint is violated, it adjusts the loss according to the direction defined by the comparator.

    Attributes:
        comparator (Callable[[Tensor, Number], Tensor]): A comparator function (e.g., greater than, less than) to evaluate the constraint.
        scalar (Number): The scalar value to compare the neuron value against.
        direction (int): The direction in which the constraint should adjust the model's predictions (either 1 or -1 based on the comparator).
        layer (str): The layer associated with the specified neuron.
        index (int): The index of the specified neuron within the layer.
    """

    def __init__(
        self,
        neuron_name: str,
        comparator: Callable[[Tensor, Number], Tensor],
        scalar: Number,
        name: str = None,
        descriptor: Descriptor = None,
        rescale_factor: float = 1.5,
    ) -> None:
        """
        Initializes the ScalarConstraint with the given neuron name, comparator, scalar value, and other optional parameters.

        Args:
            neuron_name (str): The name of the neuron that the constraint applies to.
            comparator (Callable[[Tensor, Number], Tensor]): The comparator function used to evaluate the constraint (e.g., ge, le, gt, lt).
            scalar (Number): The scalar value that the neuron value is compared to.
            name (str, optional): A custom name for the constraint. If not provided, a name is generated based on the neuron name, comparator, and scalar.
            descriptor (Descriptor, optional): The descriptor that maps neurons to layers. If not provided, the global descriptor is used.
            rescale_factor (float, optional): A factor that scales the influence of the constraint on the overall loss. Defaults to 1.5.

        Raises:
            ValueError: If the comparator function is not one of the supported comparison operators (ge, le, gt, lt).
        """

        # Compose constraint name
        name = f"{neuron_name}_{comparator.__name__}_{str(scalar)}"

        # Init parent class
        super().__init__({neuron_name}, name, rescale_factor)

        # Init variables
        self.comparator = comparator
        self.scalar = scalar

        if descriptor != None:
            self.descriptor = descriptor
            self.run_init_descriptor()

        # Get layer name and feature index from neuron_name
        self.layer = self.descriptor.neuron_to_layer[neuron_name]
        self.index = self.descriptor.neuron_to_index[neuron_name]

        # If comparator function is not supported, raise error
        if comparator not in [ge, le, gt, lt]:
            raise ValueError(
                f"Comparator {str(comparator)} used for constraint {name} is not supported. Only ge, le, gt, lt are allowed."
            )

        # Calculate directions based on constraint operator
        if self.comparator in [lt, le]:
            self.direction = 1
        elif self.comparator in [gt, ge]:
            self.direction = -1

    def check_constraint(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        """
        Checks if the constraint is satisfied based on the model's predictions.

        The constraint is evaluated by applying the comparator to the value of the specified neuron and the scalar value.

        Args:
            prediction (dict[str, Tensor]): A dictionary of model predictions, indexed by layer names.

        Returns:
            dict[str, Tensor]: A dictionary containing the constraint satisfaction result for the specified layer.
        """

        result = ~self.comparator(prediction[self.layer][:, self.index], self.scalar)

        return {self.layer: result}

    def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        """
        Calculates the direction in which the model's predictions need to be adjusted to satisfy the constraint.

        The direction is determined by the comparator and represents either a positive or negative adjustment.

        Args:
            prediction (dict[str, Tensor]): A dictionary of model predictions, indexed by layer names.

        Returns:
            dict[str, Tensor]: A dictionary containing the direction for each layer or neuron, to adjust the model's predictions.
        """

        output = zeros(
            prediction[self.layer].size(),
            device=prediction[self.layer].device,
        )
        output[:, self.index] = self.direction

        return {self.layer: output}


class BinaryConstraint(Constraint):
    """
    A class representing a binary constraint between two neurons in a neural network.

    This class checks and enforces a constraint between two neurons using a
    comparator function. The constraint is applied between two neurons located
    in different layers of the neural network. The class also calculates the
    direction for gradient adjustment based on the comparator.

    Attributes:
        neuron_name_left (str): The name of the first neuron involved in the constraint.
        neuron_name_right (str): The name of the second neuron involved in the constraint.
        comparator (Callable[[Tensor, Number], Tensor]): A function that compares the values of the two neurons.
        layer_left (str): The layer name for the first neuron.
        layer_right (str): The layer name for the second neuron.
        index_left (int): The index of the first neuron within its layer.
        index_right (int): The index of the second neuron within its layer.
        direction_left (float): The normalized direction for gradient adjustment of the first neuron.
        direction_right (float): The normalized direction for gradient adjustment of the second neuron.
    """

    def __init__(
        self,
        neuron_name_left: str,
        comparator: Callable[[Tensor, Number], Tensor],
        neuron_name_right: str,
        name: str = None,
        descriptor: Descriptor = None,
        rescale_factor: float = 1.5,
    ) -> None:
        """
        Initializes the binary constraint with two neurons, a comparator, and other configuration options.

        Args:
            neuron_name_left (str): The name of the first neuron in the constraint.
            comparator (Callable[[Tensor, Number], Tensor]): A function that compares the values of the two neurons.
            neuron_name_right (str): The name of the second neuron in the constraint.
            name (str, optional): The name of the constraint. If not provided, a default name is generated.
            descriptor (Descriptor, optional): The descriptor containing the mapping of neurons to layers.
            rescale_factor (float, optional): A factor to rescale the constraint value. Default is 1.5.
        """

        # Compose constraint name
        name = f"{neuron_name_left}_{comparator.__name__}_{neuron_name_right}"

        # Init parent class
        super().__init__({neuron_name_left, neuron_name_right}, name, rescale_factor)

        # Init variables
        self.comparator = comparator

        if descriptor != None:
            self.descriptor = descriptor
            self.run_init_descriptor()

        # Get layer name and feature index from neuron_name
        self.layer_left = self.descriptor.neuron_to_layer[neuron_name_left]
        self.layer_right = self.descriptor.neuron_to_layer[neuron_name_right]
        self.index_left = self.descriptor.neuron_to_index[neuron_name_left]
        self.index_right = self.descriptor.neuron_to_index[neuron_name_right]

        # If comparator function is not supported, raise error
        if comparator not in [ge, le, gt, lt]:
            raise RuntimeError(
                f"Comparator {str(comparator)} used for constraint {name} is not supported. Only ge, le, gt, lt are allowed."
            )

        # Calculate directions based on constraint operator
        if self.comparator in [lt, le]:
            self.direction_left = -1
            self.direction_right = 1
        else:
            self.direction_left = 1
            self.direction_right = -1

        # Normalize directions
        normalized_directions = normalize(
            tensor([self.direction_left, self.direction_right]).type(float32),
            p=2,
            dim=0,
        )
        self.direction_left = normalized_directions[0]
        self.direction_right = normalized_directions[1]

    def check_constraint(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        """
        Checks whether the binary constraint is satisfied between the two neurons.

        This function applies the comparator to the output values of the two neurons
        and returns a Boolean result for each neuron.

        Args:
            prediction (dict[str, Tensor]): A dictionary containing the predictions for each layer.

        Returns:
            dict[str, Tensor]: A dictionary with the layer names as keys and the constraint satisfaction results as values.
        """

        result = ~self.comparator(
            prediction[self.layer_left][:, self.index_left],
            prediction[self.layer_right][:, self.index_right],
        )

        return {self.layer_left: result, self.layer_right: result}

    def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        """
        Calculates the direction for gradient adjustment for both neurons involved in the constraint.

        The directions are normalized and represent the direction in which the constraint should be enforced.

        Args:
            prediction (dict[str, Tensor]): A dictionary containing the predictions for each layer.

        Returns:
            dict[str, Tensor]: A dictionary with the layer names as keys and the direction vectors as values.
        """

        output_left = zeros(
            prediction[self.layer_left].size(),
            device=prediction[self.layer_left].device,
        )
        output_left[:, self.index_left] = self.direction_left

        output_right = zeros(
            prediction[self.layer_right].size(),
            device=prediction[self.layer_right].device,
        )
        output_right[:, self.index_right] = self.direction_right

        return {self.layer_left: output_left, self.layer_right: output_right}


# FIXME
class SumConstraint(Constraint):
    def __init__(
        self,
        neuron_names_left: list[str],
        comparator: Callable[[Tensor, Number], Tensor],
        neuron_names_right: list[str],
        weights_left: list[float] = None,
        weights_right: list[float] = None,
        name: str = None,
        descriptor: Descriptor = None,
        rescale_factor: float = 1.5,
    ) -> None:

        # Init parent class
        super().__init__(
            set(neuron_names_left) & set(neuron_names_right), name, rescale_factor
        )

        # Init variables
        self.comparator = comparator

        if descriptor != None:
            self.descriptor = descriptor
            self.run_init_descriptor()

        # Get layer names and feature indices from neuron_name
        self.layers_left = []
        self.indices_left = []
        for neuron_name in neuron_names_left:
            self.layers_left.append(self.descriptor.neuron_to_layer[neuron_name])
            self.indices_left.append(self.descriptor.neuron_to_index[neuron_name])

        self.layers_right = []
        self.indices_right = []
        for neuron_name in neuron_names_right:
            self.layers_right.append(self.descriptor.neuron_to_layer[neuron_name])
            self.indices_right.append(self.descriptor.neuron_to_index[neuron_name])

        # If comparator function is not supported, raise error
        if comparator not in [ge, le, gt, lt]:
            raise ValueError(
                f"Comparator {str(comparator)} used for constraint {name} is not supported. Only ge, le, gt, lt are allowed."
            )

        # If feature list dimensions don't match weight list dimensions, raise error
        if weights_left and (len(neuron_names_left) != len(weights_left)):
            raise ValueError(
                "The dimensions of neuron_names_left don't match with the dimensions of weights_left."
            )
        if weights_right and (len(neuron_names_right) != len(weights_right)):
            raise ValueError(
                "The dimensions of neuron_names_right don't match with the dimensions of weights_right."
            )

        # If weights are provided for summation, transform them to Tensors
        if weights_left:
            self.weights_left = FloatTensor(weights_left)
        else:
            self.weights_left = ones(len(neuron_names_left))
        if weights_right:
            self.weights_right = FloatTensor(weights_right)
        else:
            self.weights_right = ones(len(neuron_names_right))

        # Calculate directions based on constraint operator
        if self.comparator in [lt, le]:
            self.direction_left = -1
            self.direction_right = 1
        else:
            self.direction_left = 1
            self.direction_right = -1

        # Normalize directions
        normalized_directions = normalize(
            tensor(self.direction_left, self.direction_right), p=2, dim=0
        )
        self.direction_left = normalized_directions[0]
        self.direction_right = normalized_directions[1]

    def check_constraint(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        raise NotImplementedError
        # # TODO remove the dynamic to device conversion and do this in initialization one way or another
        # weighted_sum_left = (
        #     prediction[layer_left][:, index_left]
        #     * self.weights_left.to(prediction[layer_left].device)
        # ).sum(dim=1)
        # weighted_sum_right = (
        #     prediction[layer_right][:, index_right]
        #     * self.weights_right.to(prediction[layer_right].device)
        # ).sum(dim=1)

        # result = ~self.comparator(weighted_sum_left, weighted_sum_right)

        # return {layer_left: result, layer_right: result}
        pass

    def calculate_direction(self, prediction: dict[str, Tensor]) -> Dict[str, Tensor]:
        raise NotImplementedError
        # # TODO move this to constructor somehow
        # layer_left = prediction.neuron_to_layer[self.neuron_name_left]
        # layer_right = prediction.neuron_to_layer[self.neuron_name_right]
        # index_left = prediction.neuron_to_index[self.neuron_name_left]
        # index_right = prediction.neuron_to_index[self.neuron_name_right]

        # output_left = zeros(
        #     prediction[layer_left].size(),
        #     device=prediction[layer_left].device,
        # )
        # output_left[:, index_left] = self.direction_left

        # output_right = zeros(
        #     prediction.layer_to_data[layer_right].size(),
        #     device=prediction.layer_to_data[layer_right].device,
        # )
        # output_right[:, index_right] = self.direction_right

        # return {layer_left: output_left, layer_right: output_right}
        pass
