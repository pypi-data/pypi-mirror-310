from sklearn.cluster import KMeans
from .forest import CrossClusterForest


class SingleDatasetForest:
    """
    Wrapper for CrossClusterForest that handles single dataset input.
    This version automatically clusters a single training dataset instead
    of requiring pre-clustered data.
    """

    def __init__(self, ntree=100, merged_ntree=500, outcome_col='y', k=10):
        """
        Parameters:
        -----------
        ntree : int
            Number of trees in cluster-specific random forests
        merged_ntree : int
            Number of trees in merged random forest
        outcome_col : str
            Name of outcome column
        k : int
            Number of clusters for k-means
        """
        self.model = CrossClusterForest(
            ntree=ntree,
            merged_ntree=merged_ntree,
            outcome_col=outcome_col,
            k=k,
            cluster_ind=1
        )
        self.k = k
        self.outcome_col = outcome_col

    def fit(self, X, y=None):
        """
        Fit model on single dataset.

        Parameters:
        -----------
        X : pandas.DataFrame
            Training data including features
        y : pandas.Series, optional
            If provided, will be used as outcome. Otherwise,
            outcome_col must exist in X
        """
        # Prepare data
        if y is not None:
            data = X.copy()
            data[self.outcome_col] = y
        else:
            if self.outcome_col not in X.columns:
                raise ValueError(f"outcome_col '{self.outcome_col}' not found in X")
            data = X.copy()

        # Cluster the data
        kmeans = KMeans(n_clusters=self.k, n_init=25)
        cluster_labels = kmeans.fit_predict(
            data.drop(self.outcome_col, axis=1)
        )

        # Create list of clusters
        clusters_list = []
        for i in range(self.k):
            cluster_data = data[cluster_labels == i]
            if len(cluster_data) > 2:  # Keep clusters with > 2 samples
                clusters_list.append(cluster_data)

        # Fit the model
        self.model.fit(clusters_list, ncoef=X.shape[1])
        return self

    def predict(self, X, method='stack_ridge'):
        """
        Make predictions using specified method.

        Parameters:
        -----------
        X : pandas.DataFrame
            Features to predict on
        method : str
            One of: 'merged', 'unweighted', 'stack_ridge', 'stack_lasso'
        """
        return self.model.predict(X, method=method)