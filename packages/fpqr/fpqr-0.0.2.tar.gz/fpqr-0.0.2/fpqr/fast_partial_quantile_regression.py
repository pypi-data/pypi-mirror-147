import logging
import sys

import numpy as np
from scipy.linalg import pinv
import asgl

from . import quantile_covariances as qc

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FPQRegression:
    def __init__(self, quantile=0.5, n_components=2, metric='li', solver='MOSEK'):
        """
        :param quantile: quantile of interest
        :param n_components: Number of components to keep. Should be in [1, min(n_samples, n_features, n_targets)].
        :param metric: should be one of 'li', 'choi', 'dodge'. Default is 'li' which generally provides the
                       fastest and best results
        """
        self.quantile = quantile
        self.n_components = n_components
        self.metric = metric
        self.solver = solver
        self.valid_metrics = ['li', 'dodge', 'choi']
        self.x_mean_ = None
        self.x_weights_ = None
        self.y_weights_ = None
        self.x_scores_ = None
        self.y_scores_ = None
        self.x_loadings_ = None
        self.y_loadings_ = None
        self.x_rotations_ = None
        self.y_rotations_ = None
        self.coef_ = None
        self.intercept_ = None

    def _center_matrix(self, x):
        x_mean = x.mean(axis=0)
        x2 = x - x_mean
        return x2, x_mean

    def _svd_flip_1d(self, u, v):
        """
        Inplace sign flip for consistency across solvers and archs
        Parameters
        ----------
        u array of weights
        v array of weights
        Returns
        -------
        u, v with the sign updated
        """
        biggest_abs_val_idx = np.argmax(np.abs(u))
        sign = np.sign(u[biggest_abs_val_idx])
        u *= sign
        v *= sign
        return u, v

    def _check_constant_residuals(self, x, tol=1e-8):
        bool_constant_residual = True
        for j in range(x.shape[1]):
            if np.any(np.abs(x[:, j]) > tol):
                bool_constant_residual = False
                break
        return bool_constant_residual

    def fit(self, x, y):
        """
        PLS as an SVD problem.
        Here the y_weights are normalized
        """
        eps = np.finfo(x.dtype).eps
        if y.ndim == 1:
            y = y.reshape(-1, 1)
        n = x.shape[0]
        p = x.shape[1]
        q = y.shape[1]
        if not 1 <= self.n_components <= p:
            logging.error(f'n_components ({self.n_components}) should be in [1, min(n_samples, n_features, n_targets)]')
            raise ValueError(f'n_components ({self.n_components}) should be in [1, min(n_samples, n_features, '
                             f'n_targets)]')
        if self.metric not in self.valid_metrics:
            logging.error(f'Invalid metric. Valid metrics are: {self.valid_metrics}')
            raise ValueError(f'Invalid metric. Valid metrics are: {self.valid_metrics}')
        # Center data
        xk, self.x_mean_ = self._center_matrix(x)
        yk, _y_mean = self._center_matrix(y)
        self.x_weights_ = np.zeros((p, self.n_components))  # W
        self.y_weights_ = np.zeros((q, self.n_components))  # Q
        self.x_scores_ = np.zeros((n, self.n_components))  # T
        self.y_scores_ = np.zeros((n, self.n_components))  # U
        self.x_loadings_ = np.zeros((p, self.n_components))  # P
        self.y_loadings_ = np.zeros((q, self.n_components))  # Delta
        for k in range(self.n_components):
            # Check if residuals are constant
            bool_xk_constant = self._check_constant_residuals(xk)
            if bool_xk_constant:
                logging.warning(f'Constant residuals on matrix xk at iteration {k + 1}')
            bool_yk_constant = self._check_constant_residuals(yk)
            if bool_yk_constant:
                logging.warning(f'Constant residuals on matrix yk at iteration {k + 1}')
            qcov_xy = np.zeros((p, q))
            for q_iter in range(yk.shape[1]):
                qcov = qc.QuantileCovariance(quantile=self.quantile, metric=self.metric, solver=self.solver)
                qcov_xy[:, q_iter] = qcov.fit(x=xk, y=yk[:, q_iter])
            u, d, v = np.linalg.svd(qcov_xy, full_matrices=False)
            x_weights = u[:, 0]
            y_weights = v[0, :]
            # Inplace sign flip for consistency across solvers and archs
            x_weights, y_weights = self._svd_flip_1d(x_weights, y_weights)
            x_scores = np.dot(xk, x_weights)
            y_scores = np.dot(yk, y_weights)
            # Deflation: subtract rank-one approx to obtain xk+1 and yk+1
            x_loadings = np.dot(x_scores, xk) / (np.dot(x_scores, x_scores) + eps)
            xk -= np.outer(x_scores, x_loadings)
            # regress yk on x_score
            y_loadings = np.dot(x_scores, yk) / (np.dot(x_scores, x_scores) + eps)
            yk -= np.outer(x_scores, y_loadings)
            # Store results
            self.x_weights_[:, k] = x_weights  # W
            self.y_weights_[:, k] = y_weights  # Q
            self.x_scores_[:, k] = x_scores  # T
            self.y_scores_[:, k] = y_scores  # U
            self.x_loadings_[:, k] = x_loadings  # P
            self.y_loadings_[:, k] = y_loadings  # Delta
            logging.debug(f"component {k+1} computed")
        # Compute transformation matrices (rotations). See User Guide.
        self.x_rotations_ = np.dot(self.x_weights_,
                                   pinv(np.dot(self.x_loadings_.T, self.x_weights_), check_finite=False))
        self.y_rotations_ = np.dot(self.y_weights_,
                                   pinv(np.dot(self.y_loadings_.T, self.y_weights_), check_finite=False))
        # Obtain coef_
        coef_ = np.zeros((p, q))
        intercept_ = np.zeros((1, q))
        qr_model = asgl.ASGL(model='qr', penalization=None, tau=self.quantile, solver=self.solver)
        for i in range(y.shape[1]):
            qr_model.fit(self.x_scores_, y[:, i])
            coef_[:, i] = np.dot(self.x_rotations_, qr_model.coef_[0][1:])
            intercept_[0, i] = qr_model.coef_[0][0]
        self.coef_ = coef_
        self.intercept_ = intercept_

    def predict(self, x):
        """
        Obtain predictions. First center x_new. Then perform p = b0 + X_center @ b
        Parameters
        ----------
        Returns prediction
        """
        x_new = x - self.x_mean_
        prediction = self.intercept_ + np.dot(x_new, self.coef_)
        return prediction
