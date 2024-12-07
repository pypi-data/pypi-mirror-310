import logging
from typing import Union
from torch import Tensor
from torch.nn import Module
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer

from .core import CGGDModule
from .constraints import Constraint
from .descriptor import Descriptor


class Learner(CGGDModule):
    def __init__(
        self,
        network: Module,
        descriptor: Descriptor,
        constraints: list[Constraint],
        loss_function: Union[_Loss, dict[str, _Loss]],
        optimizer: Optimizer,
    ):
        """
        A class that integrates a neural network with a training and validation loop,
        supporting single or multi-output loss functions. The class manages the forward pass,
        training step, and validation step while also configuring the optimizer.

        Args:
            network (Module): The neural network model to be trained.
            descriptor (Descriptor): An object that defines the structure of the network,
                                    including the output layers.
            constraints (list[Constraint]): A list of constraints that can be applied during training.
            loss_function (Union[_Loss, dict[str, _Loss]]): A loss function or a dictionary of loss functions
                                                        for each output layer.
            optimizer (Optimizer): The optimizer used for training the model.

        Raises:
            ValueError: If the descriptor does not contain any output layers or if the number of loss functions
                        does not match the number of output layers when using a dictionary of loss functions.
        """

        # Init parent class
        super().__init__(descriptor, constraints)

        # Init object variables
        self.network = network
        self.descriptor = descriptor
        self.loss_function = loss_function
        self.optimizer = optimizer

        # Perform checks
        if len(self.descriptor.output_layers) == 0:
            raise ValueError(
                'The descriptor class must contain one or more output layers. Mark a layer as output by setting descriptor.add("layer", ..., output=True).'
            )

        if isinstance(loss_function, _Loss):
            if len(self.descriptor.output_layers) > 1:
                logging.warning(
                    f"Multiple layers were marked as output, but only one loss function is defined. Only the loss of layer {list(self.descriptor.output_layers)[0]} will be calculated and used. To use the same loss function for all output layers, please specify then explicitly."
                )

        if isinstance(loss_function, dict):
            if len(self.descriptor.output_layers) != len(loss_function):
                raise ValueError(
                    f"The number of marked output layers does not match the number of provided loss functions."
                )

        # Assign proper step function based on if one or multiple loss functions are assigned
        if isinstance(loss_function, _Loss):
            self.training_step = self.training_step_single
            self.validation_step = self.validation_step_single

        if isinstance(loss_function, dict):
            self.training_step = self.training_step_multi
            self.validation_step = self.validation_step_multi

    def forward(self, x):
        """
        Perform a forward pass through the network.

        Args:
            x (Tensor): The input tensor to pass through the network.

        Returns:
            Tensor: The model's output for the given input.
        """

        return self.network(x)

    def training_step_single(self, batch, batch_idx):
        """
        Perform a single training step using a single loss function.

        Args:
            batch (tuple): A tuple containing the input and target output tensors.
            batch_idx (int): The index of the batch in the current epoch.

        Returns:
            Tensor: The loss value for the batch.
        """

        self.train()

        inputs, outputs = batch
        prediction: dict[str, Tensor] = self(inputs)

        layer = list(self.descriptor.output_layers)[0]
        loss = self.loss_function(prediction[layer], outputs)

        self.log(
            "train_loss",
            loss,
            on_step=False,
            on_epoch=True,
        )

        return super().training_step(prediction, loss)

    def training_step_multi(self, batch, batch_idx):
        """
        Perform a training step using multiple loss functions, one for each output layer.

        Args:
            batch (tuple): A tuple containing the input and target output tensors.
            batch_idx (int): The index of the batch in the current epoch.

        Returns:
            Tensor: The total loss value for the batch, combining the losses from all output layers.
        """

        self.train()

        inputs, outputs = batch
        prediction: dict[str, Tensor] = self(inputs)

        # TODO add hyperparameter to scale loss per function
        loss = 0
        for layer in self.descriptor.output_layers:
            layer_loss = self.loss_function[layer](prediction[layer], outputs)
            loss += layer_loss

            self.log(
                f"train_loss_{layer}",
                layer_loss,
                on_step=False,
                on_epoch=True,
            )

        self.log(
            "train_loss",
            loss,
            on_step=False,
            on_epoch=True,
        )

        return super().training_step(prediction, loss)

    def validation_step_single(self, batch, batch_idx):
        """
        Perform a single validation step using a single loss function.

        Args:
            batch (tuple): A tuple containing the input and target output tensors.
            batch_idx (int): The index of the batch in the current epoch.

        Returns:
            Tensor: The validation loss for the batch.
        """

        self.eval()

        inputs, outputs = batch
        prediction: dict[str, Tensor] = self(inputs)

        layer = list(self.descriptor.output_layers)[0]
        loss = self.loss_function(prediction[layer], outputs)

        self.log(
            "valid_loss",
            loss,
            on_step=False,
            on_epoch=True,
        )

        return super().validation_step(prediction, loss)

    def validation_step_multi(self, batch, batch_idx):
        """
        Perform a validation step using multiple loss functions, one for each output layer.

        Args:
            batch (tuple): A tuple containing the input and target output tensors.
            batch_idx (int): The index of the batch in the current epoch.

        Returns:
            Tensor: The total validation loss for the batch, combining the losses from all output layers.
        """

        self.eval()

        inputs, outputs = batch
        prediction: dict[str, Tensor] = self(inputs)

        loss = 0
        for layer in self.descriptor.output_layers:
            layer_loss = self.loss_function[layer](prediction[layer], outputs)
            loss += layer_loss

            self.log(
                f"valid_loss_{layer}",
                layer_loss,
                on_step=False,
                on_epoch=True,
            )

        self.log(
            "valid_loss",
            loss,
            on_step=False,
            on_epoch=True,
        )

        return super().validation_step(prediction, loss)

    def configure_optimizers(self):
        """
        Configure the optimizer for training.

        Returns:
            Optimizer: The optimizer used to update the model's parameters during training.
        """

        return self.optimizer
