from torch import Tensor, tensor, sum, numel
from torchmetrics import Metric

# NOTE


class ConstraintSatisfactionRatio(Metric):
    """
    A custom metric to calculate the ratio of satisfied constraints in a neural network model.
    It computes the proportion of constraints that have been satisfied,
    where satisfaction is determined based on the provided constraint results.

    This metric tracks the number of unsatisfied constraints and the total number of constraints
    during the training process, and computes the ratio of satisfied constraints once all updates
    have been made.

    Attributes:
        unsatisfied (Tensor): Tracks the number of unsatisfied constraints.
        total (Tensor): Tracks the total number of constraints processed.

    Note:
        For more information about custom metrics, we refer to the Pytorch Lightning documentation
        at https://lightning.ai/docs/torchmetrics/stable/pages/implement.html
    """

    def __init__(self, **kwargs):
        """
        Initializes the ConstraintSatisfactionRatio metric by setting up the
        state variables to track the number of unsatisfied and total constraints.

        Args:
            **kwargs: Additional arguments to pass to the base Metric class constructor.
        """

        # Init parent class
        super().__init__(**kwargs)

        # Init scalar tensors that will hold metric values
        self.add_state("unsatisfied", default=tensor(0), dist_reduce_fx="sum")
        self.add_state("total", default=tensor(0), dist_reduce_fx="sum")

    def update(self, constraint_result: Tensor) -> None:
        """
        Updates the state of the metric with the latest constraint results.

        Args:
            constraint_result (Tensor): A tensor representing the result of
                                         the constraint checks, where each
                                         element indicates whether a constraint
                                         is satisfied (e.g., 0 for satisfied,
                                         1 for unsatisfied).
        """
        self.unsatisfied += sum(constraint_result)
        self.total += numel(constraint_result)

    def compute(self) -> Tensor:
        """
        Computes the constraint satisfaction ratio, defined as:
        1 - (number of unsatisfied constraints / total constraints).

        Returns:
            Tensor: The satisfaction ratio as a scalar tensor.
        """
        return 1 - (self.unsatisfied.float() / self.total)
