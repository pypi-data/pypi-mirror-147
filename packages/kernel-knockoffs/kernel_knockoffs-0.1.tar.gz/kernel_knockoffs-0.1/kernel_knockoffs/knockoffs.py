"""
Implementation of algorithm 1 of paper Model-Free Feature
Screening and FDR Control with Knockoff Features with metrics
PC, HSIC and cMMD.

"""


import numpy as np
import numpy.typing as npt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import (
    check_X_y,
    check_array,
    check_is_fitted,
)

from .utils import get_equi_features, top_k
from . import association_measures as am


association_measures = [
    "cMMD",
    "DC",
    "HSIC",
    "lasso",
    "PC",
    "pearson_correlation",
    "TR",
]
kernel_association_measures = ["cMMD", "HSIC"]
kernels = ["distance", "gaussian", "linear"]


class KernelKnockoffs(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        alpha: float = 1.0,
        association_measure: str = "lasso",
        kernel: str = "linear",
        normalized: bool = False,
        normalize_input: bool = True,
        random_state: float = None,
        p_screened_samples: float = 0.5,
        n_screened_features: int = 10,
    ) -> None:
        super().__init__()

        assert (
            association_measure in association_measures
        ), "Unavailable association_measure"
        assert kernel in kernels, "Unavailable kernel"

        self.alpha = alpha
        self.association_measure = association_measure
        self.kernel = kernel
        self.normalized = normalized
        self.normalize_input = normalize_input
        self.random_state = random_state
        self.p_screened_samples = p_screened_samples
        self.n_screened_features = n_screened_features

    def compute_association(self, X, y):

        args = {}
        if self.association_measure in kernel_association_measures:
            args["kernel"] = self.kernel
            if self.association_measure == "HSIC":
                args["normalized"] = self.normalized

        if self.normalize_input:
            X = X / np.linalg.norm(X, ord=2, axis=0)

        assoc_func = self.get_association_measure()
        assoc = assoc_func(X, y, **args)
        # nans are at the end when sorting
        assoc[np.isnan(assoc)] = -float("inf")

        return assoc

    def fit(
        self,
        X: npt.ArrayLike,
        y: npt.ArrayLike,
    ):
        """Fits model in a supervised manner following algorithm 1 in the paper
        *Model-free Feature Screening and FDR Control with Knockoff Features*
        by Liu et Al (2021).
        If d < n2 / 2 we do not perform the screening set to reduce the data.

        Parameters
        ----------
        X : numpy array like object where the rows correspond to the samples
            and the columns to features.

        y : numpy array like, which can be multi-dimensional.

        Returns
        -------
        Itself.
        """

        np.random.seed(self.random_state)

        X, y = check_X_y(X, y)
        X = X.copy()
        y = np.expand_dims(y, axis=1)

        n_samples, self.n_features_in_ = X.shape
        stop, samples_screening, samples_inference, msg = misc_checks(
            n_samples, self.p_screened_samples, self.n_screened_features
        )

        if stop:
            print(msg)
            self.alpha_indices_ = []
            self.n_features_out_ = 0
            return self

        if self.n_features_in_ > (n_samples / 2):
            print(f"Screening best {self.n_screened_features} features")
            X_screening, y_screening = X[samples_screening, :], y[samples_screening]

            screen_assoc = self.compute_association(X_screening, y_screening)
            screened_features = top_k(screen_assoc, self.n_screened_features)

            X_inference, y_inference = (
                X[np.ix_(samples_inference, screened_features)],
                y[samples_inference],
            )

        else:
            X_inference, y_inference = X, y

            if self.normalize_input:
                X_inference = X_inference / np.linalg.norm(X_inference, ord=2, axis=0)

            screened_features = np.arange(self.n_features_in_)

        # computing knockoffs
        n_features = X_inference.shape[1]
        X_knockoff = get_equi_features(X_inference)

        # knockoff statistic
        assoc = self.compute_association(
            np.hstack((X_inference, X_knockoff)), y_inference
        )

        betas = assoc[0:n_features]
        betas_knockoff = assoc[n_features:]
        self.w_ = betas - betas_knockoff

        # fdr control
        idx, self.t_alpha_ = self.fdr_selection(self.w_, self.alpha)
        self.selected_ = screened_features[idx]
        self.w_ = self.w_[idx]

        return self

    def fdr_selection(self, w, alpha):
        """
        Computes the selected features with respect to alpha.

        Parameters
        ----------
        alpha : threshold value to use for post inference selection.

        Returns
        -------
        A 3 element tuple where:
            1 - indices corresponding to indexes of the chosen features in
            the original array.
            2 - the threshold value.
            3 - the number of selected features.

        """

        ts = np.sort(abs(w))

        def fraction_3_6(t):
            num = (self.w_ <= -abs(t)).sum() + 1
            den = max((self.w_ >= abs(t)).sum(), 1)
            return num / den

        fraction_3_6_v = np.vectorize(fraction_3_6)
        fdp = fraction_3_6_v(ts)

        t_alpha_ = np.where(fdp <= alpha)
        if t_alpha_[0].size == 0:
            # no one selected..
            t_alpha_min = np.inf
        else:
            t_alpha_min = min(ts[t_alpha_])
        # alpha_indices_ = self.screened_features_[np.where(w >= t_alpha_min)[0]]
        idx = np.where(w >= t_alpha_min)[0]

        return idx, t_alpha_

    def transform(self, X, y=None):
        """Transforms an input dataset X into the reduce set of features
        given by the alpha_indices found by the fit method.

        Parameters
        ----------
        X : numpy array like object where the rows correspond to the samples
            and the columns to features.

        y : numpy array like, which can be multi-dimensional.

        Returns
        -------
        A sliced X where we only retain the selected features.
        """
        check_is_fitted(self, attributes=["selected_"])
        X = check_array(X)
        msg = "Same shape for fit and transform"
        assert self.n_features_in_ == X.shape[1], msg
        return X[:, self.selected_]

    def fit_transform(self, X, y, **fit_params):
        """Fits and transforms an input dataset X and y.

        Parameters
        ----------
        X : numpy array like object where the rows correspond to the samples
            and the columns to features.

        y : numpy array like, which can be multi-dimensional.

        Returns
        -------
        The new version of X corresponding to the selected features.
        """

        return self.fit(X, y, **fit_params).transform(X, y)

    def get_association_measure(self):
        """Returns the correct association measure
        given the attribute in __init__.
        """
        match self.association_measure:
            case "PC":
                f = am.projection_corr
            case "TR":
                f = am.tr
            case "HSIC":
                f = am.HSIC
            case "cMMD":
                f = am.cMMD
            case "DC":
                f = am.distance_corr
            case "pearson_correlation":
                f = am.pearson_correlation
            case "lasso":
                f = am.Lasso
            case _:
                error_msg = f"associative measure undefined {self.association_measure}"
                raise ValueError(error_msg)

        return f

    def _more_tags(self):
        return {"stateless": True}


def misc_checks(n, n1, d):
    """
    Checks a variety of things with respect to n, n1 and d.
    """
    set_one, set_two = None, None
    stop = False
    msg = ""

    if n in [1, 2, 3]:
        # not possible because we want d < n / 2
        msg = "Fit is not possible, data too small and \
can't satisfy condition d < n_2 / 2"
        stop = True

    n2 = n - int(n1 * n)
    # need to check
    if d >= n2 / 2:
        # d not set correctly so we set it to the highest plausible value
        d = n2 / 2 - 1
        if d <= 0:
            msg = "Fit is not possible, data too small and \
can't satisfy condition d < n_2 / 2"
            stop = True
        else:
            msg = "d badly set, reseting"
    if not stop:
        msg = "Splitting the data"
        # split data
        indices = np.arange(n)
        np.random.shuffle(indices)
        set_one = indices[: int(n1 * n)]
        set_two = indices[int(n1 * n) :]

    return stop, set_one, set_two, msg
