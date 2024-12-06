"""
Cross-Cluster Weighted Forests

A package implementing the Cross-Cluster Weighted Forests method
for ensemble learning across multiple data clusters or studies.
"""

from .models.forest import CrossClusterForest, evaluate_model
from .models.wrapper import SingleDatasetForest
from .data_generation.simulation import sim_data
from .visualization.plots import plot_results, interpret_results
from .models.stacking import create_stacking_model

__version__ = "0.1.0"

__all__ = [
    "CrossClusterForest",
    "SingleDatasetForest",
    "evaluate_model",
    "sim_data",
    "plot_results",
    "interpret_results",
    "create_stacking_model"
]