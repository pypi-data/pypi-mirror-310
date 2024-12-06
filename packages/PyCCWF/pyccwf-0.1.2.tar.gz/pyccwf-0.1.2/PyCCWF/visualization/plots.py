import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np


def plot_results(improvements):
    """
    Plot performance comparison of different methods.

    Parameters:
    -----------
    improvements : dict
        Dictionary of improvements from evaluate_model()
    """
    methods = list(improvements.keys())
    values = list(improvements.values())

    # Create color mapping
    colors = {
        'merged': 'gray',
        'unweighted': 'lightblue',
        'stack_ridge': 'purple',
        'stack_lasso': 'purple'
    }

    plt.figure(figsize=(10, 6))
    bars = plt.bar(methods, values, color=[colors[m] for m in methods])

    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.xticks(range(len(methods)), methods, rotation=45, ha='right')
    plt.ylabel('% change in RMSE from baseline RF')
    plt.title('Performance Comparison of Different Methods')

    legend_elements = [
        Patch(facecolor='gray', label='Baseline RF'),
        Patch(facecolor='lightblue', label='Naive Ensemble'),
        Patch(facecolor='purple', label='Stacking')
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()


def interpret_results(improvements):
    """
    Print interpretation of results.

    Parameters:
    -----------
    improvements : dict
        Dictionary of improvements from evaluate_model()
    """
    print("\nPerformance Analysis:")
    print("-" * 50)

    print("\nRelative Reduction in RMSE over Merged Model (%):")
    for method, imp in improvements.items():
        print(f"{method:12s}: {imp:6.2f}%")

    best_method = min(
        improvements.items(),
        key=lambda x: x[1] #if x[0] != 'merged' else -float('inf')
    )
    print(f"\nBest performing method: {best_method[0]} ({best_method[1]:.2f}%)")