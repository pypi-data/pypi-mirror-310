from .dataset import DataSet
from .charts import (
    bar,
    line,
    scatter,
    pie,
    histogram
)

__version__ = "0.1.0"

# Export main classes and functions
__all__ = [
    "DataSet",
    "bar",
    "line",
    "scatter",
    "pie",
    "histogram"
]
