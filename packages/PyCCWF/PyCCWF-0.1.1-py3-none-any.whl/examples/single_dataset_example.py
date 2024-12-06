import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from PyCCWF import (
    SingleDatasetForest,
    plot_results,
    interpret_results
)


def generate_example_data(n_samples=1000, n_features=20):
    """Generate example dataset for demonstration"""
    np.random.seed(42)

    # Generate features
    X = np.random.randn(n_samples, n_features)

    # Generate target with non-linear relationships
    y = (np.sum(X, axis=1) +
         0.5 * X[:, 0] ** 2 +
         0.3 * X[:, 0] * X[:, 1] +
         np.random.randn(n_samples) * 0.1)

    # Create DataFrame
    data = pd.DataFrame(
        X,
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    data['target'] = y

    return data


def run_single_dataset_example():
    n_features = 20
    """Run example using single dataset"""
    print("Generating example data...")
    data = generate_example_data(n_samples=1000, n_features=n_features)

    # Split into train and test
    train_data, test_data = train_test_split(
        data,
        test_size=0.2,
        random_state=42
    )

    print("\nFitting Cross-cluster Weighted Forest...")
    model = SingleDatasetForest(
        ntree=100,
        merged_ntree=500,
        outcome_col='target',
        k=10
    )

    # Option 1: Pass complete DataFrame
    print("\nFitting model...")
    model.fit(train_data)

    # Option 2: Pass X and y separately
    # X_train = train_data.drop('target', axis=1)
    # y_train = train_data['target']
    # model.fit(X_train, y_train)

    # Make predictions using different methods
    methods = ['merged', 'unweighted', 'stack_ridge', 'stack_lasso']
    results = {}
    predictions_dict = {}

    print("\nEvaluating methods...")
    for method in methods:
        predictions = model.predict(test_data, method=method)
        rmse = np.sqrt(np.mean((test_data['target'] - predictions) ** 2))
        results[method] = rmse
        predictions_dict[method] = predictions
    predictions_df = pd.DataFrame.from_dict(predictions_dict)
    performance_df = pd.DataFrame([results])
    # Calculate improvements
    baseline_rmse = results['merged']

    improvements = {
        method: (rmse-baseline_rmse) / baseline_rmse * 100
        for method, rmse in results.items()
    }

    # Plot and interpret results
    print("\nPlotting results...")
    plot_results(improvements)
    interpret_results(improvements)

    return model, improvements, predictions_df, performance_df


if __name__ == "__main__":
    model, improvements, predictions, performance = run_single_dataset_example()
    print("\nRMSE's per method")
    print(performance)