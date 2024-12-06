import numpy as np
from PyCCWF import (
    CrossClusterForest,
    sim_data,
    plot_results,
    interpret_results,
    evaluate_model
)


def run_example():
    """Run complete example with train/test split"""
    # Set random seed
    np.random.seed(42)

    # Parameters
    n_clusters = 10
    n_test = 5
    n_features = 20
    samples_per_cluster = 200
    k = 10

    print("Generating simulation data...")
    data = sim_data(
        nclusters=n_clusters,
        ncoef=n_features,
        ntest=n_test,
        multimodal=True,
        n_samples=samples_per_cluster,
        clustszind=2
    )
    clusters_list = data['clusters_list']

    # Split into train and test clusters
    train_clusters = clusters_list[:-n_test]
    test_clusters = clusters_list[-n_test:]

    print("\nStudy sizes:")
    print(f"Training clusters: {len(train_clusters)}")
    print(f"Test clusters: {len(test_clusters)}")
    for i, study in enumerate(train_clusters):
        print(f"Training study {i + 1}: {len(study)} samples")
    for i, study in enumerate(test_clusters):
        print(f"Test study {i + 1}: {len(study)} samples")

    # Initialize and fit model
    print("\nFitting Cross-cluster Weighted Forest...")
    model = CrossClusterForest(
        ntree=100,
        merged_ntree=500,
        outcome_col='y',
        k=k,
        cluster_ind=1
    )

    # Fit on training clusters only
    print("\nFitting on training data...")
    model.fit(train_clusters, ncoef=n_features)

    # Evaluate on test clusters
    print("\nEvaluating on test clusters...")
    eval_mod = evaluate_model(
        model,
        test_clusters,
    )
    predictions, improvements, performance = eval_mod['predictions'], eval_mod['improvements'], eval_mod['performance']

    # Plot and interpret results
    print("\nPlotting results...")
    plot_results(improvements)
    interpret_results(improvements)

    return model, improvements, predictions, performance


if __name__ == "__main__":
    model, improvements, predictions, performance = run_example()
    print("\nRMSE's per method")
    print(performance)
