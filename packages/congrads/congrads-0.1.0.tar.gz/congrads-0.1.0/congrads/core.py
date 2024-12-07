import logging
from typing import Dict
from lightning import LightningModule
from torch import Tensor, float32, no_grad, norm, tensor
from torchmetrics import Metric
from torch.nn import ModuleDict

from .constraints import Constraint
from .metrics import ConstraintSatisfactionRatio
from .descriptor import Descriptor


class CGGDModule(LightningModule):
    """
    A PyTorch Lightning module that integrates constraint-guided optimization into the training and validation steps.

    This module extends the `LightningModule` and incorporates constraints on the neural network's predictions 
    by adjusting the loss using a rescale factor. The constraints are checked, and the loss is modified to guide 
    the optimization process based on these constraints.

    Attributes:
        descriptor (Descriptor): The object that describes the layers and neurons of the network, including 
                                 the categorization of variable layers.
        constraints (list[Constraint]): A list of constraints that define the conditions to guide the optimization.
        train_csr (Dict[str, Metric]): A dictionary of `ConstraintSatisfactionRatio` metrics to track constraint satisfaction 
                                       during training, indexed by constraint name.
        valid_csr (Dict[str, Metric]): A dictionary of `ConstraintSatisfactionRatio` metrics to track constraint satisfaction 
                                       during validation, indexed by constraint name.
    """

    def __init__(self, descriptor: Descriptor, constraints: list[Constraint]):
        """
        Initializes the CGGDModule with a descriptor and a list of constraints.

        Args:
            descriptor (Descriptor): The object that describes the network's layers and neurons, including their categorization.
            constraints (list[Constraint]): A list of constraints that will guide the optimization process.

        Raises:
            Warning if there are no variable layers in the descriptor, as constraints will not be applied.
        """

        # Init parent class
        super().__init__()

        # Init object variables
        self.descriptor = descriptor
        self.constraints = constraints

        # Perform checks
        if len(self.descriptor.variable_layers) == 0:
            logging.warning(
                "The descriptor object has no variable layers. The constraint guided loss adjustment is therefore not used. Is this the intended behaviour?"
            )

        # Assign descriptor to constraints
        for constraint in self.constraints:
            constraint.descriptor = descriptor
            constraint.run_init_descriptor()

        # Init constraint metric logging
        self.train_csr: Dict[str, Metric] = ModuleDict(
            {
                constraint.constraint_name: ConstraintSatisfactionRatio()
                for constraint in self.constraints
            }
        )
        self.train_csr["global"] = ConstraintSatisfactionRatio()
        self.valid_csr: Dict[str, Metric] = ModuleDict(
            {
                constraint.constraint_name: ConstraintSatisfactionRatio()
                for constraint in self.constraints
            }
        )
        self.valid_csr["global"] = ConstraintSatisfactionRatio()

    def training_step(
        self,
        prediction: dict[str, Tensor],
        loss: Tensor,
    ):
        """
        The training step where the standard loss is combined with rescale loss based on the constraints.

        For each constraint, the satisfaction ratio is checked, and the loss is adjusted by adding a rescale loss
        based on the directions calculated by the constraint.

        Args:
            prediction (dict[str, Tensor]): The model's predictions for each layer.
            loss (Tensor): The base loss from the model's forward pass.

        Returns:
            Tensor: The combined loss, including both the original loss and the rescale loss from the constraints.
        """

        # Init scalar tensor for loss
        total_rescale_loss = tensor(0, dtype=float32, device=self.device)

        # Compute rescale loss without tracking gradients
        with no_grad():

            # For each constraint, TODO split into real and validation only constraints
            for constraint in self.constraints:

                # Check if constraints are satisfied and calculate directions
                constraint_checks = constraint.check_constraint(prediction)
                constraint_directions = constraint.calculate_direction(prediction)

                # Only do direction calculations for variable layers affecting constraint
                for layer in constraint.layers & self.descriptor.variable_layers:

                    # Multiply direction modifiers with constraint result
                    constraint_result = (
                        constraint_checks[layer].unsqueeze(1).type(float32)
                        * constraint_directions[layer]
                    )

                    # Multiply result with rescale factor o constraint
                    constraint_result *= constraint.rescale_factor

                    # Calculate gradients of general loss for each sample
                    loss.backward(retain_graph=True, inputs=prediction[layer])
                    loss_grad = prediction[layer].grad

                    # Calculate loss gradient norm
                    norm_loss_grad = norm(loss_grad, dim=0, p=2, keepdim=True)

                    # Calculate rescale loss
                    rescale_loss = (
                        (prediction[layer] * constraint_result * norm_loss_grad)
                        .sum()
                        .abs()
                    )

                    # Store rescale loss for this reference space
                    total_rescale_loss += rescale_loss

                    # Log constraint satisfaction ratio
                    # NOTE does this take into account spaces with different dimensions?
                    self.train_csr[constraint.constraint_name](constraint_checks[layer])
                    self.train_csr["global"](constraint_checks[layer])
                    self.log(
                        f"train_csr_{constraint.constraint_name}_{layer}",
                        self.train_csr[constraint.constraint_name],
                        on_step=False,
                        on_epoch=True,
                    )

        # Log global constraint satisfaction ratio
        self.log(
            "train_csr_global",
            self.train_csr["global"],
            on_step=False,
            on_epoch=True,
        )

        # Return combined loss
        return loss + total_rescale_loss

    def validation_step(
        self,
        prediction: dict[str, Tensor],
        loss: Tensor,
    ):
        """
        The validation step where the satisfaction of constraints is checked without applying the rescale loss.

        Similar to the training step, but without updating the loss, this method tracks the constraint satisfaction 
        during validation.

        Args:
            prediction (dict[str, Tensor]): The model's predictions for each layer.
            loss (Tensor): The base loss from the model's forward pass.

        Returns:
            Tensor: The base loss value for validation.
        """

        # Compute rescale loss without tracking gradients
        with no_grad():

            # For each constraint in this reference space, calculate directions
            for constraint in self.constraints:

                # Check if constraints are satisfied for
                constraint_checks = constraint.check_constraint(prediction)

                # Only do direction calculations for variable layers affecting constraint
                for layer in constraint.layers & self.descriptor.variable_layers:

                    # Log constraint satisfaction ratio
                    # NOTE does this take into account spaces with different dimensions?
                    self.valid_csr[constraint.constraint_name](constraint_checks[layer])
                    self.valid_csr["global"](constraint_checks[layer])
                    self.log(
                        f"valid_csr_{constraint.constraint_name}",
                        self.valid_csr[constraint.constraint_name],
                        on_step=False,
                        on_epoch=True,
                    )

        # Log global constraint satisfaction ratio
        self.log(
            "valid_csr_global",
            self.valid_csr["global"],
            on_step=False,
            on_epoch=True,
        )

        # Return loss
        return loss
