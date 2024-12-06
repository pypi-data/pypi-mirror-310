import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge, Lasso
from ..models.clustering import create_clusters
from ..models.stacking import create_stacking_model


class CrossClusterForest:
    """
    Cross-Cluster Weighted Forest implementation with key ensemble methods.
    """

    def __init__(self, ntree=100, merged_ntree=500, outcome_col='y', k=10, cluster_ind=1):
        """
        Parameters:
        -----------
        ntree : int
            Number of trees in cluster-specific random forests
        merged_ntree : int
            Number of trees in merged random forest (default 500)
        outcome_col : str
            Name of outcome column (default 'y')
        k : int
            Number of clusters for k-means (used if cluster_ind=1)
        cluster_ind : int
            Whether to use k-means clustering (1) or original clusters/data partitions included in inputted cluster_list (0)
        """
        self.ntree = ntree
        self.merged_ntree = merged_ntree
        self.outcome_col = outcome_col
        self.k = k
        self.cluster_ind = cluster_ind
        self.cluster_models_ = None
        self.merged_model_ = None
        self.stack_ridge_ = None
        self.stack_lasso_ = None

    def _create_base_model(self, data, is_merged=False):
        """
        Create a random forest with R-like defaults; this performs better than scikit defaults

        Parameters:
        -----------
        data : pandas.DataFrame
            Training data
        is_merged : bool
            Whether this is the merged model (uses merged_ntree if True)
        """
        p = data.drop(self.outcome_col, axis=1).shape[1]
        n = data.shape[0]

        return RandomForestRegressor(
            n_estimators=self.merged_ntree if is_merged else self.ntree,
            n_jobs=-1,
            min_samples_leaf=5,
            max_features=max(p // 3, 1),
            bootstrap=True,
            max_samples=n,
            min_impurity_decrease=0,
            max_depth=None,
            min_samples_split=2
        )

    def fit(self, clusters_list, ncoef=None):
        """
        Fit the Cross-cluster Weighted Forest model.

        Parameters:
        -----------
        clusters_list : list of pandas.DataFrame
            List of training data clusters
        ncoef : int, optional
            Number of coefficients/features (needed if cluster_ind=1)

        Returns:
        --------
        self : returns an instance of self
        """
        # Verify outcome column exists in all clusters
        for i, cluster in enumerate(clusters_list):
            if self.outcome_col not in cluster.columns:
                raise ValueError(
                    f"Outcome column '{self.outcome_col}' not found in cluster {i}"
                )

        # Create clusters if needed
        if self.cluster_ind == 1:
            # Create clusters with ntest=0 since we're only working with training data
            clusters_dict = create_clusters(
                clusters_list=clusters_list,
                ntest=0,
                k=self.k
            )
            clusters_list = clusters_dict['clusters_list']

        # Fit merged model
        merged_data = pd.concat(clusters_list).reset_index(drop=True)
        self.merged_model_ = self._create_base_model(merged_data, is_merged=True)
        self.merged_model_.fit(
            merged_data.drop(self.outcome_col, axis=1),
            merged_data[self.outcome_col]
        )

        # Fit individual cluster models
        self.cluster_models_ = []
        allpreds = [[] for _ in range(len(clusters_list))]

        # Train individual models
        for j in range(len(clusters_list)):
            # Fit model on cluster j
            model = self._create_base_model(clusters_list[j])
            model.fit(
                clusters_list[j].drop(self.outcome_col, axis=1),
                clusters_list[j][self.outcome_col]
            )
            self.cluster_models_.append(model)

            # Make predictions on all training datasets
            for i in range(len(clusters_list)):
                newdata = clusters_list[i].drop(self.outcome_col, axis=1)
                preds = model.predict(newdata)

                if len(allpreds[i]) == 0:
                    allpreds[i] = preds.reshape(-1, 1)
                else:
                    allpreds[i] = np.column_stack([allpreds[i], preds])


        # Stack predictions
        predstack = np.vstack([pred for pred in allpreds])
        y_stack = np.concatenate([cluster[self.outcome_col] for cluster in clusters_list])

        self.stack_ridge_ = create_stacking_model(predstack, y_stack, method='ridge', intercept=True)
        self.stack_ridge_.fit(predstack, y_stack)
        self.stack_lasso_ = create_stacking_model(predstack, y_stack, method='lasso', intercept=True)
        self.stack_lasso_.fit(predstack, y_stack)

        return self

    def predict(self, X, method='merged'):
        """
        Make predictions using specified method.

        Parameters:
        -----------
        X : pandas.DataFrame
            Features to predict on
        method : str
            One of: 'merged', 'unweighted', 'stack_ridge', 'stack_lasso'

        Returns:
        --------
        numpy.ndarray : Predictions
        """
        if not isinstance(X, pd.DataFrame):
            raise ValueError("X must be a pandas DataFrame")

        X = X.drop(self.outcome_col, axis=1, errors='ignore')

        if method == 'merged':
            return self.merged_model_.predict(X)

        # Get predictions from all cluster models
        cluster_preds = np.column_stack([
            model.predict(X) for model in self.cluster_models_
        ])

        if method == 'unweighted':
            return np.mean(cluster_preds, axis=1)
        elif method == 'stack_ridge':
            return self.stack_ridge_.predict(cluster_preds)
        elif method == 'stack_lasso':
            return self.stack_lasso_.predict(cluster_preds)
        else:
            raise ValueError(
                "method must be one of: 'merged', 'unweighted', "
                "'stack_ridge', 'stack_lasso'"
            )

def evaluate_model(model, test_clusters):
    """
    Evaluate model performance on test clusters.

    Parameters:
    -----------
    model : CrossClusterForest
        Fitted model
    train_clusters : list
        Training clusters
    test_clusters : list
        Test clusters
    ncoef : int, optional
        Number of features (needed if cluster_ind=1)

    Returns:
    --------
    dict : Dictionary of improvements over merged model
    """
    methods = ['merged', 'unweighted', 'stack_ridge', 'stack_lasso']
    method_rmses = {method: [] for method in methods}
    predictions_dict = {}

    for test_data in test_clusters:
        for method in methods:
            preds = model.predict(test_data, method=method)
            predictions_dict[method] = preds
            if model.outcome_col in test_data.columns:
                rmse = np.sqrt(np.mean((test_data[model.outcome_col] - preds) ** 2))
                method_rmses[method].append(rmse)

    predictions_df = pd.DataFrame.from_dict(predictions_dict)
    # Calculate improvements, if we have outcome information for the test set:
    improvements = {}
    if model.outcome_col in test_data.columns:
        merged_rmse = np.mean(method_rmses['merged'])
        for method in methods:
            method_rmse = np.mean(method_rmses[method])
            imp = (method_rmse - merged_rmse) / merged_rmse * 100
            improvements[method] = imp
        method_rmses = pd.DataFrame.from_dict(method_rmses)

    return {'predictions': predictions_df, 'improvements': improvements, 'performance': method_rmses}