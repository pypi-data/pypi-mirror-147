import logging
import sys

import asgl
import numpy as np
from sklearn.preprocessing import scale

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class QuantileCovariance:
    def __init__(self, quantile=0.5, metric='li', solver='MOSEK'):
        """
        :param quantile: quantile of interest
        :param metric: should be one of 'li', 'choi', 'dodge'. Default is 'li' which generally provides the
                       fastest and best results
        """
        self.quantile = quantile
        self.metric = metric
        self.solver = solver

    def _wrap_qr_model(self, x, y, y_response=True):
        """
        Compute the quantile regression slope between a matrix x and a vector y. Used in Dodge and Choi qcov computation
        :param x: data matrix
        :param y: response vector y
        :param y_response: indicate if y works as response or as predictor.
        """
        qr_model = asgl.ASGL(model='qr', penalization=None, intercept=True, tau=self.quantile, solver=self.solver)
        qr_slope = []
        if y_response:
            y = y.reshape(-1)
            for j in range(x.shape[1]):
                qr_model.fit(x=x[:, j].reshape((-1, 1)), y=y)
                qr_slope = np.append(qr_slope, qr_model.coef_[0][1])
        else:
            for j in range(x.shape[1]):
                qr_model.fit(x=y.reshape((-1, 1)), y=x[:, j])
                qr_slope = np.append(qr_slope, qr_model.coef_[0][1])
        return qr_slope

    def _cov_dodge(self, x, y):
        """
        :param x: data matrix
        :param y: response vector y
        :return: quantile covariance in the sense of Dodge 2009
        """
        # Solve the univariate y ~ xi problem, suited for singular matrices
        qr_slope = self._wrap_qr_model(x, y, y_response=True)
        if x.shape[1] == 1:
            results = np.cov(x.T) * qr_slope
        else:
            results = np.diag(np.cov(x.T)) * qr_slope
        return results

    def _cov_choi(self, x, y):
        """
        :param x: data matrix
        :param y: response vector y
        :return: quantile covariance metric in the sense of Choi 2018
        """
        qr_slope_y_on_x = self._wrap_qr_model(x, y, y_response=True)
        qr_slope_x_on_y = self._wrap_qr_model(x, y, y_response=False)
        # Quantile correlation
        tmp_results = np.sqrt(np.maximum(qr_slope_x_on_y * qr_slope_y_on_x, 0))
        tmp_results = np.sign(qr_slope_x_on_y) * tmp_results
        # Quantile covariance
        if x.shape[1] == 1:
            sqrt_var_term = np.sqrt(np.cov(x.T) * np.var(y))
        else:
            sqrt_var_term = np.sqrt(np.diag(np.cov(x.T)) * np.var(y))
        results = tmp_results * sqrt_var_term
        return results

    def _cov_li(self, x, y):
        """
        :param x: data matrix
        :param y: response vector y
        :return: quantile covariance metric in the sense of Li 2015
        """
        n_obs = x.shape[0]
        psi_value = self.quantile - (y - np.quantile(y, self.quantile) < 0)
        x_center = scale(x, with_std=False)
        results = (1.0 / n_obs) * np.dot(psi_value.T, x_center)
        return results

    def fit(self, x, y):
        if self.metric == 'li':
            cov = self._cov_li(x, y)
        elif self.metric == 'dodge':
            cov = self._cov_dodge(x, y)
        elif self.metric == 'choi':
            cov = self._cov_choi(x, y)
        else:
            logging.error('metric should be either li, choi or dodge')
            raise ValueError('metric should be either li, choi or dodge')
        return cov
