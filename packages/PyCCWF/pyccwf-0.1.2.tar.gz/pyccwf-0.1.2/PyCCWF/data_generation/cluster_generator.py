import numpy as np
from scipy.stats import ortho_group, multivariate_normal, chi2
from scipy.spatial.distance import mahalanobis
import warnings
from sklearn.preprocessing import StandardScaler


class AdvancedClusterGenerator:
    """Advanced cluster generator that mimics R package genRandomClust functionality"""

    def __init__(self, cov_method="eigen"):
        """
        Initialize cluster generator.

        Parameters:
        -----------
        cov_method : str
            Method for generating correlation matrices ("eigen", "onion", or "unifcorrmat")
        """
        self.cov_method = cov_method

    def generate_cluster_sizes(self, clustszind, num_clusters, clustSizeEq=None,
                               rangeN=None, clustSizes=None):
        """
        Generate cluster sizes following R's logic.

        Parameters:
        -----------
        clustszind : int
            1: Different sizes, random from rangeN
            2: Equal sizes (clustSizeEq)
            3: Different sizes (specified in clustSizes)
        num_clusters : int
            Number of clusters to generate
        clustSizeEq : int
            Size for each cluster if clustszind=2
        rangeN : tuple
            (min, max) for random cluster sizes if clustszind=1
        clustSizes : list
            Specific sizes for each cluster if clustszind=3
        """
        if clustszind == 1:
            if rangeN is None:
                raise ValueError("rangeN must be specified for clustszind=1")
            return np.random.randint(rangeN[0], rangeN[1], size=num_clusters)

        elif clustszind == 2:
            if clustSizeEq is None:
                raise ValueError("clustSizeEq must be specified for clustszind=2")
            return [clustSizeEq] * num_clusters

        elif clustszind == 3:
            if clustSizes is None or len(clustSizes) != num_clusters:
                raise ValueError("clustSizes must be specified for clustszind=3")
            return clustSizes

        else:
            raise ValueError("clustszind must be 1, 2, or 3")

    def generate_correlation_matrix(self, dim, method=None):
        """
        Generate random correlation matrix using various methods.

        Parameters:
        -----------
        dim : int
            Dimension of correlation matrix
        method : str
            Method to use (eigen, onion, or unifcorrmat)

        Returns:
        --------
        numpy.ndarray : Generated correlation matrix
        """
        method = method or self.cov_method

        if method == "eigen":
            # Generate random eigenvalues
            eigs = np.random.uniform(0.1, 2, size=dim)
            eigs = eigs / np.sum(eigs) * dim

            # Generate random orthogonal matrix
            Q = ortho_group.rvs(dim)

            # Construct correlation matrix
            C = Q @ np.diag(eigs) @ Q.T

            # Ensure diagonal is 1
            D = np.diag(1 / np.sqrt(np.diag(C)))
            C = D @ C @ D

        elif method == "onion":
            # Implementation of onion method
            C = np.eye(dim)
            for i in range(1, dim):
                x = np.random.normal(0, 1, dim - i)
                x = x / np.linalg.norm(x)
                y = np.zeros(dim)
                y[i:] = x
                C[i:, i - 1] = y[i:]
                C[i - 1, i:] = y[i:]
            C = (C + C.T) / 2

        else:  # unifcorrmat
            C = np.eye(dim)
            for i in range(dim):
                for j in range(i + 1, dim):
                    r = np.random.uniform(-1, 1)
                    C[i, j] = r
                    C[j, i] = r

            # Ensure positive definiteness
            while not self._is_positive_definite(C):
                C = (C + np.eye(dim)) / 2

        return C

    def _is_positive_definite(self, matrix):
        """Check if matrix is positive definite"""
        try:
            np.linalg.cholesky(matrix)
            return True
        except np.linalg.LinAlgError:
            return False

    def generate_multimodal_component(self, n_samples, n_features, n_modes=2):
        """
        Generate multimodal distribution within a cluster.

        Parameters:
        -----------
        n_samples : int
            Number of samples to generate
        n_features : int
            Number of features
        n_modes : int
            Number of modes in the distribution

        Returns:
        --------
        numpy.ndarray : Generated multimodal data
        """
        samples_per_mode = np.random.multinomial(n_samples,
                                                 [1 / n_modes] * n_modes)

        centers = np.random.normal(0, 0.5, (n_modes, n_features))
        data = []

        for i in range(n_modes):
            cov = self.generate_correlation_matrix(n_features)
            cov *= 0.3
            mode_data = multivariate_normal.rvs(
                mean=centers[i],
                cov=cov,
                size=samples_per_mode[i]
            )
            data.append(mode_data)

        return np.vstack(data)

    def adjust_separation_by_dimension(self, separation, num_features):
        """
        Adjust separation criterion based on dimensionality.

        Parameters:
        -----------
        separation : float
            Requested separation
        num_features : int
            Number of features

        Returns:
        --------
        float : Adjusted separation criterion
        """
        dim_factor = np.sqrt(chi2.ppf(0.95, num_features) / num_features)
        adjusted_sep = separation / dim_factor

        if adjusted_sep > np.sqrt(num_features):
            warnings.warn(
                f"Requested separation {separation} might be unrealistic in "
                f"{num_features} dimensions. Consider reducing separation or "
                f"increasing number of features. Adjusted separation: {adjusted_sep:.2f}"
            )

        return adjusted_sep

    def generate_outliers(self, n_outliers, n_features, data, labels):
        """
        Generate outliers using Mahalanobis distance.

        Parameters:
        -----------
        n_outliers : int
            Number of outliers to generate
        n_features : int
            Number of features
        data : numpy.ndarray
            Original data
        labels : numpy.ndarray
            Cluster labels

        Returns:
        --------
        numpy.ndarray : Generated outliers
        """
        # Calculate global statistics
        global_mean = np.mean(data, axis=0)
        global_cov = np.cov(data.T)
        global_cov_inv = np.linalg.pinv(global_cov)

        # Calculate cluster-specific statistics
        unique_labels = np.unique(labels)
        cluster_stats = []
        for label in unique_labels:
            cluster_data = data[labels == label]
            cluster_mean = np.mean(cluster_data, axis=0)
            cluster_cov = np.cov(cluster_data.T)
            cluster_cov_inv = np.linalg.pinv(cluster_cov)
            cluster_stats.append({
                'mean': cluster_mean,
                'cov': cluster_cov,
                'cov_inv': cluster_cov_inv
            })

        # Generate different types of outliers
        n_types = 3
        outliers_per_type = n_outliers // n_types
        outliers = []

        # Type 1: Mahalanobis-based outliers
        maha_outliers = []
        attempts = 0
        max_attempts = 1000

        while len(maha_outliers) < outliers_per_type and attempts < max_attempts:
            candidate = multivariate_normal.rvs(
                mean=global_mean,
                cov=global_cov * 4
            )

            is_outlier = True
            for stats in cluster_stats:
                maha_dist = mahalanobis(
                    candidate,
                    stats['mean'],
                    stats['cov_inv']
                )
                threshold = np.sqrt(chi2.ppf(0.999, n_features))

                if maha_dist < threshold:
                    is_outlier = False
                    break

            if is_outlier:
                maha_outliers.append(candidate)

            attempts += 1

        outliers.append(np.array(maha_outliers))

        # Type 2: Uniform outliers
        data_range = np.ptp(data, axis=0)
        expansion_factor = 1.5
        uniform_outliers = np.random.uniform(
            low=np.min(data, axis=0) - expansion_factor * data_range,
            high=np.max(data, axis=0) + expansion_factor * data_range,
            size=(outliers_per_type, n_features)
        )

        verified_uniform = []
        for outlier in uniform_outliers:
            is_valid = True
            for stats in cluster_stats:
                maha_dist = mahalanobis(
                    outlier,
                    stats['mean'],
                    stats['cov_inv']
                )
                if maha_dist < np.sqrt(chi2.ppf(0.99, n_features)):
                    is_valid = False
                    break
            if is_valid:
                verified_uniform.append(outlier)

        outliers.append(np.array(verified_uniform))

        # Type 3: Mixture-based outliers
        mix_outliers = []
        for _ in range(outliers_per_type):
            c1, c2 = np.random.choice(len(cluster_stats), 2, replace=False)
            alpha = np.random.uniform(1.5, 2.0)
            beta = 1 - alpha

            point = (alpha * cluster_stats[c1]['mean'] +
                     beta * cluster_stats[c2]['mean'])

            is_valid = True
            for stats in cluster_stats:
                maha_dist = mahalanobis(
                    point,
                    stats['mean'],
                    stats['cov_inv']
                )
                if maha_dist < np.sqrt(chi2.ppf(0.99, n_features)):
                    is_valid = False
                    break

            if is_valid:
                mix_outliers.append(point)

        outliers.append(np.array(mix_outliers))

        combined_outliers = np.vstack([arr for arr in outliers if arr.size > 0])

        while len(combined_outliers) < n_outliers:
            candidate = multivariate_normal.rvs(
                mean=global_mean,
                cov=global_cov * 5
            )
            is_outlier = True
            for stats in cluster_stats:
                maha_dist = mahalanobis(
                    candidate,
                    stats['mean'],
                    stats['cov_inv']
                )
                if maha_dist < np.sqrt(chi2.ppf(0.999, n_features)):
                    is_outlier = False
                    break
            if is_outlier:
                combined_outliers = np.vstack([combined_outliers, candidate])

        return combined_outliers[:n_outliers]

    def generate_clusters(self, num_clusters, num_features, clustszind=2,
                          clustSizeEq=None, rangeN=None, clustSizes=None,
                          separation=0.8, num_noisy=0, range_var=(1, 10),
                          multimodal=True, num_modes=2):
        """
        Generate clusters with full functionality.

        Parameters:
        -----------
        [All parameters from original R genRandomClust implementation with documentation]

        Returns:
        --------
        tuple : (data, labels, outliers)
        """
        adjusted_separation = self.adjust_separation_by_dimension(
            separation, num_features
        )

        sizes = self.generate_cluster_sizes(
            clustszind, num_clusters, clustSizeEq, rangeN, clustSizes
        )

        correlations = [self.generate_correlation_matrix(num_features + num_noisy)
                        for _ in range(num_clusters)]

        variances = [np.random.uniform(*range_var, size=num_features + num_noisy)
                     for _ in range(num_clusters)]

        centers = []
        max_attempts = 1000
        attempts = 0

        while len(centers) < num_clusters and attempts < max_attempts:
            candidate = np.random.normal(0, 1, num_features)
            candidate = candidate / np.linalg.norm(candidate)

            if not centers or all(np.linalg.norm(candidate - c[:num_features]) >= adjusted_separation
                                  for c in centers):
                centers.append(np.pad(candidate, (0, num_noisy)))

            attempts += 1

        if len(centers) < num_clusters:
            warnings.warn(
                f"Could only generate {len(centers)} separated clusters with "
                f"adjusted separation {adjusted_separation:.2f} in {num_features} dimensions"
            )

        centers = np.array(centers)

        data_list = []
        labels_list = []

        for i in range(num_clusters):
            if multimodal:
                cluster_data = self.generate_multimodal_component(
                    sizes[i], num_features + num_noisy, num_modes
                )
            else:
                cluster_data = multivariate_normal.rvs(
                    mean=np.zeros(num_features + num_noisy),
                    cov=correlations[i],
                    size=sizes[i]
                )

            cluster_data = cluster_data * np.sqrt(variances[i]) + centers[i]

            data_list.append(cluster_data)
            labels_list.extend([i] * sizes[i])

        data = np.vstack(data_list)
        labels = np.array(labels_list)

        outliers = self.generate_outliers(
            n_outliers=50,
            n_features=num_features + num_noisy,
            data=data,
            labels=labels
        )

        return data, labels, outliers