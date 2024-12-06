import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from .cluster_generator import AdvancedClusterGenerator

def generate_complex_outcome(X, coefs, icoefs):
    """
    Generate complex outcome variable with non-linear relationships.
    """
    n_samples = X.shape[0]

    # Linear terms
    y = np.dot(X, coefs)

    # Quadratic terms
    y += icoefs[0] * X[:, 0] ** 2 + icoefs[1] * X[:, 1] ** 2

    # Interaction terms
    y += icoefs[0] * X[:, 0] * X[:, 1]  # Positive interaction
    y -= icoefs[1] * X[:, 0] * X[:, 2]  # Negative interaction

    # Additional non-linear terms
    y += 0.5 * np.sin(X[:, 0] * 2)  # Sinusoidal effect
    y += 0.3 * np.exp(X[:, 1] / 4)  # Exponential effect

    # Add heteroscedastic noise
    noise_scale = 0.1 * (1 + np.abs(X[:, 0]))  # Noise increases with X0
    y += np.random.normal(0, noise_scale, n_samples)

    return y

def sim_data(nclusters, ncoef, ntest, multimodal=True, n_samples=100, clustszind=2):
    """
    Simulate multiple studies with complex data structures.
    """
    clusters_list = []
    nchoose = 10
    n_noise = 5

    # Initialize advanced cluster generator
    generator = AdvancedClusterGenerator(cov_method="eigen")

    # Generate coefficients
    pos_coefs = np.random.uniform(0.5, 5, size=nchoose - nchoose // 2)
    neg_coefs = np.random.uniform(-5, -0.5, size=nchoose // 2)
    coefs = np.concatenate([neg_coefs, pos_coefs])
    np.random.shuffle(coefs)

    # Select variables
    vars_idx = np.random.choice(range(ncoef), size=nchoose, replace=False)

    # Interaction coefficients
    icoefs = np.array([4, 1.8])

    # Generate training data
    train_data, train_labels, train_outliers = generator.generate_clusters(
        num_clusters=nclusters,
        num_features=ncoef - n_noise,
        clustszind=clustszind,
        clustSizeEq=n_samples,
        rangeN=(n_samples-50, n_samples+50),
        separation=0.8,
        num_noisy=n_noise,
        range_var=(1, 10),
        multimodal=multimodal,
        num_modes=2
    )

    # Generate test data
    test_data, test_labels, test_outliers = generator.generate_clusters(
        num_clusters=ntest,
        num_features=ncoef - n_noise,
        clustszind=2,
        clustSizeEq=500,
        separation=0.8,
        num_noisy=n_noise,
        range_var=(1, 10),
        multimodal=multimodal,
        num_modes=2
    )

    # Scale outliers
    scaler = StandardScaler()
    train_outliers = scaler.fit_transform(train_outliers)

    # Split outliers for each study
    outliers_per_study = np.array_split(train_outliers, nclusters)

    # Generate studies
    for i in range(nclusters + ntest):
        # Generate slightly varied coefficients
        cur_coefs = np.array([np.random.uniform(c - 0.5, c + 0.5) for c in coefs])

        if i < (nclusters):
            # Training clusters
            cluster_data = train_data[train_labels == i]
            # Add outliers
            cluster_data = np.vstack([cluster_data, outliers_per_study[i]])
            # Scale data
            cluster_data = StandardScaler().fit_transform(cluster_data)
        else:
            # Test studies
            test_idx = i - nclusters
            cluster_data = test_data[test_labels == test_idx]
            cluster_data = StandardScaler().fit_transform(cluster_data)

        # Generate outcome (y)
        X = cluster_data[:, vars_idx]
        y = generate_complex_outcome(X, cur_coefs, icoefs)

        # Create DataFrame
        cluster_df = pd.DataFrame(
            np.column_stack([y, cluster_data]),
            columns=['y'] + [f'V{i + 1}' for i in range(ncoef)]
        )

        clusters_list.append(cluster_df)

    return {'clusters_list': clusters_list}