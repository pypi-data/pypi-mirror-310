import numpy as np
from scipy.optimize import nnls
from sklearn.linear_model import Lasso, Ridge, LassoCV, ElasticNetCV


def create_stacking_model(X, y, method='lasso', intercept=True):
    """
    Fit a stacked regression model using different methods.

    Parameters:
    -----------
    X : array-like
        Predictor matrix
    y : array-like
        Target values
    method : str
        Method for computing coefficients ('lasso', 'ridge')
    intercept : bool
        Whether to include intercept

    Returns:
    --------
    tuple : (coefficients, intercept)
    """

    def generate_lambda_sequence(X, y, n_lambda=100, lambda_min_ratio=1e-4):
        n, p = X.shape
        lambda_max = np.max(np.abs(X.T @ y)) / n
        lambda_min = lambda_min_ratio * lambda_max
        return np.logspace(np.log10(lambda_max), np.log10(lambda_min), num=n_lambda)

    if method == 'lasso':
        model = LassoCV(
            alphas=generate_lambda_sequence(X, y),
            fit_intercept=intercept,
            precompute='auto',
            max_iter=100000,
            tol=1e-7,
            copy_X=True,
            cv=10,
            verbose=False,
            n_jobs=None,
            positive=True,
            random_state=None,
            selection='cyclic'
            )
        return model

    elif method == 'ridge':
        # model = ElasticNetCV(
        #     l1_ratio=[0.01],  # This makes it close to Ridge
        #     alphas=generate_lambda_sequence(X, y, lambda_min_ratio=1e-3) * 100,
        #     fit_intercept=intercept,
        #     max_iter=100000,
        #     tol=1e-7,
        #     cv=10,
        #     positive=True,
        #     random_state=None
        # )
        model = Ridge(alpha=1.0, positive=True, fit_intercept=intercept)
        return model

    else:
        raise ValueError(f"Unknown method: {method}")
