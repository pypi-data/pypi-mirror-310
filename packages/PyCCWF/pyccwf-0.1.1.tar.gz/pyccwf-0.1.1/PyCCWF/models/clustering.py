import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def create_clusters(clusters_list, ntest, k):
    """
    Create clusters using K-means clustering.

    Parameters:
    -----------
    clusters_list : list of pandas.DataFrame
        List of all cluster data
    ntest : int
        Number of test clusters to keep separate
    k : int
        Number of clusters for k-means

    Returns:
    --------
    dict : Dictionary containing new clusters list
    """
    if not clusters_list:
        raise ValueError("clusters_list cannot be empty")

    if ntest >= len(clusters_list):
        raise ValueError("ntest must be less than number of clusters")

    # Use all data if ntest=0, otherwise exclude test clusters
    data_for_clustering = clusters_list if ntest == 0 else clusters_list[:-ntest]

    if not data_for_clustering:
        raise ValueError("No data available for clustering after train/test split")

    # Merge clusters for clustering
    merged = pd.concat(data_for_clustering).reset_index(drop=True)
    merged = merged.sample(frac=1).reset_index(drop=True)

    print(f"\nBefore clustering - merged shape: {merged.shape}")

    # Cluster without using y
    kmeans = KMeans(n_clusters=k, n_init=25)
    cluster_labels = kmeans.fit_predict(merged.drop('y', axis=1, errors='ignore'))

    # Split into clusters
    new_clusters_list = []
    for i in sorted(np.unique(cluster_labels)):
        cluster_data = merged[cluster_labels == i]
        if len(cluster_data) > 2:  # Only keep clusters with > 2 samples
            new_clusters_list.append(cluster_data)

    print(f"Number of clusters after size filtering: {len(new_clusters_list)}")
    print(f"Sizes of retained clusters: {[len(c) for c in new_clusters_list]}")
    print(f"Total sample size after clustering: {sum([len(c) for c in new_clusters_list])}")
    # Add test studies if any
    if ntest > 0:
        new_clusters_list.extend(clusters_list[-ntest:])

    print(f"Final cluster sizes after adding optional test clusters: {[len(c) for c in new_clusters_list]}")

    return {'clusters_list': new_clusters_list}