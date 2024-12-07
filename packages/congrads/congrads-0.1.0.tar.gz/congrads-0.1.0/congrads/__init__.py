# __init__.py

# Only expose the submodules, not individual classes
from . import core
from . import constraints
from . import datasets
from . import descriptor
from . import learners
from . import metrics
from . import networks

# Define __all__ to specify that the submodules are accessible, but not classes directly.
__all__ = [
    "core",
    "constraints",
    "datasets",
    "descriptor",
    "learners",
    "metrics",
    "networks"
]