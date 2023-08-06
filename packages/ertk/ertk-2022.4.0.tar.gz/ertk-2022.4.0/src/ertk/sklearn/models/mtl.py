import liblinear.liblinearutil as liblinearutil
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, MetaEstimatorMixin
from sklearn.linear_model import LogisticRegression

from ertk.sklearn.utils import OneVsRestClassifier

_EPS = 1e-15


class BaseBinaryMTFL(BaseEstimator):
    """Linear regressor based on MTFL. Code adapted from
    https://github.com/argyriou/multi_task_learning

    Parameters
    ----------
    gamma: float
        Gamma value.
    eps_init: float
        Initial value for epsilon.
    n_iters: int
        Number of iterations per step.
    """

    def __init__(
        self,
        gamma: float = 1,
        epsilon: float = 1e-4,
        n_iters: int = 10,
        loss: str = "logistic",
    ):
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_iters = n_iters
        self.loss = loss

    def _loss(self, X, y, task_idxs):
        num_tasks = len(task_idxs)
        W = np.zeros((X.shape[1], num_tasks))
        cost = 0
        err = 0
        reg = 0
        for t_id in range(num_tasks):
            task_x = X[task_idxs[t_id]]
            task_y = y[task_idxs[t_id]]

            if self.loss == "logistic":
                model = liblinearutil.train(
                    task_y, task_x, f"-s 0 -e 1e-3 -c {self.gamma} -q"
                )
                w, b = model.get_decfun()
            elif self.loss == "svm":
                model = liblinearutil.train(
                    task_y, task_x, f"-s 2 -e 1e-3 -c {self.gamma} -q"
                )
                w, b = model.get_decfun()
            elif self.loss == "ols":
                K = task_x.T @ task_x
                mat_inv = np.linalg.inv(K + self.gamma * np.eye(K.shape[0]))
                w = mat_inv @ task_x.T @ task_y

                # K = task_x @ task_x.T  # Linear kernel
                # mat_inv = np.linalg.inv(K + self.gamma * np.eye(K.shape[0]))
                # a = mat_inv @ task_x.T @ task_y
                # cost += self.gamma * task_y @ a
                # err += self.gamma**2 * a.T @ a
                # W[:, t_id] = task_x.T @ a
            w = np.asarray(w)
            W[:, t_id] = w
            _cost = self.gamma * w.T @ w
            cost += _cost
        reg = cost - err
        return W, cost, err, reg

    def Dmin(self, a):
        return a / a.sum()

    def Dmin_eps(self, a, eps):
        return self.Dmin(np.sqrt(a**2 + eps))

    def fit(self, X, y, tasks):
        self._fit_feat(X, y, tasks)
        return self

    def _fit_feat(self, X, y, tasks):
        task_ids = np.unique(tasks)
        task_idxs = [np.flatnonzero(tasks == t) for t in task_ids]
        dim = X.shape[1]
        Dini = np.eye(dim) / dim

        def fmeth(a):
            _a = np.zeros_like(a)
            _a[a > _EPS] = 1 / a[a > _EPS]
            return _a

        # train_alternating
        U, s, _ = np.linalg.svd(Dini, hermitian=True)
        fS = np.sqrt(fmeth(s))
        fS[fS > _EPS] = 1 / fS[fS > _EPS]
        fD_isqrt = U @ np.diag(fS) @ U.T
        _costs = np.empty((self.n_iters, 3))
        for i in range(self.n_iters):
            W, cost, err, reg = self._loss(X @ fD_isqrt, y, task_idxs)
            W = fD_isqrt @ W

            _costs[i] = [cost, err, reg]

            U, s, _ = np.linalg.svd(W)
            if dim > len(task_ids):
                s = np.r_[s, np.zeros(dim - len(task_ids))]
            Smin = self.Dmin_eps(s, eps=self.epsilon)
            D = U @ np.diag(Smin) @ U.T

            U, s, _ = np.linalg.svd(D, hermitian=True)
            fS = np.sqrt(fmeth(s))
            fS[fS > _EPS] = 1 / fS[fS > _EPS]
            fD_isqrt = U @ np.diag(fS) @ U.T
        # train_alternating

        s = np.linalg.svd(D, compute_uv=False)
        _costs[:, [0, 2]] = (
            _costs[:, [0, 2]] + self.gamma * self.epsilon * fmeth(s).sum()
        )
        self.mineps_ = self.epsilon
        self.W_ = W
        self.D_ = D
        self.costs_ = [_costs]

    def predict(self, X):
        return X @ self.W_


class MTFLMulticlass(BaseEstimator, ClassifierMixin):
    """Linear regressor based on MTFL. Code adapted from
    https://github.com/argyriou/multi_task_learning

    Parameters
    ----------
    gamma: float
        Gamma value.
    eps_init: float
        Initial value for epsilon.
    n_iters: int
        Number of iterations per step.
    """

    def __init__(
        self,
        gamma: float = 1,
        epsilon: float = 1e-4,
        n_iters: int = 10,
        loss: str = "logistic",
    ):
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_iters = n_iters
        self.loss = loss

    def _loss(self, X, y, task_idxs):
        num_tasks = len(task_idxs)
        classes = np.unique(y)
        W = np.zeros((len(classes), X.shape[1], num_tasks))
        cost = np.zeros(len(classes))
        err = np.zeros_like(cost)
        for t_id in range(num_tasks):
            task_x = X[task_idxs[t_id]]
            task_y = y[task_idxs[t_id]]

            task_classes = np.unique(task_y)
            if self.loss == "logistic":
                model = liblinearutil.train(
                    task_y, task_x, f"-s 0 -e 1e-3 -c {self.gamma} -q"
                )
                for i, c in enumerate(task_classes):
                    W[c, :, t_id] = model.get_decfun(label_idx=i)[0]
            elif self.loss == "svm":
                model = liblinearutil.train(
                    task_y, task_x, f"-s 2 -e 1e-3 -c {self.gamma} -q"
                )
                for i, c in enumerate(task_classes):
                    W[c, :, t_id] = model.get_decfun(label_idx=i)[0]
            _cost = self.gamma * (W[:, :, t_id] ** 2).sum(-1)
            cost += _cost
        reg = cost - err
        return W, cost, err, reg

    def Dmin(self, a):
        return a / a.sum()

    def Dmin_eps(self, a, eps):
        return self.Dmin(np.sqrt(a**2 + eps))

    def fit(self, X, y, tasks):
        self.classes_, y = np.unique(y, return_inverse=True)
        self._fit_feat(X, y, tasks)
        return self

    def _fit_feat(self, X, y, tasks):
        task_ids = np.unique(tasks)
        task_idxs = [np.flatnonzero(tasks == t) for t in task_ids]
        n_classes = len(self.classes_)
        dim = X.shape[1]
        Dini = np.tile(np.eye(dim) / dim, (n_classes, 1, 1))

        def fmeth(a):
            _a = np.zeros_like(a)
            _a[a > _EPS] = 1 / a[a > _EPS]
            return _a

        # train_alternating
        U, s, _ = np.linalg.svd(Dini, hermitian=True)
        fS = np.sqrt(fmeth(s))
        fS[fS > _EPS] = 1 / fS[fS > _EPS]
        fD_isqrt = U @ np.apply_along_axis(np.diag, 1, fS) @ U.transpose(0, 2, 1)

        _costs = np.empty((self.n_iters, n_classes, 3))
        for i in range(self.n_iters):
            W, cost, err, reg = self._loss((X @ fD_isqrt).mean(0), y, task_idxs)
            W = fD_isqrt @ W

            _costs[i] = np.c_[cost, err, reg]

            U, s, _ = np.linalg.svd(W)
            if dim > len(task_ids):
                s = np.c_[
                    s,
                    np.zeros(
                        (
                            n_classes,
                            dim - len(task_ids),
                        )
                    ),
                ]
            Smin = self.Dmin_eps(s, eps=self.epsilon)
            D = U @ np.apply_along_axis(np.diag, 1, Smin) @ U.transpose(0, 2, 1)

            U, s, _ = np.linalg.svd(D, hermitian=True)
            fS = np.sqrt(fmeth(s))
            fS[fS > _EPS] = 1 / fS[fS > _EPS]
            fD_isqrt = U @ np.apply_along_axis(np.diag, 1, fS) @ U.transpose(0, 2, 1)
        # train_alternating

        s = np.linalg.svd(D, compute_uv=False)
        _costs[:, [0, 2]] = (
            _costs[:, [0, 2]] + self.gamma * self.epsilon * fmeth(s).sum()
        )
        self.mineps_ = self.epsilon
        self.W_ = W
        self.D_ = D
        self.costs_ = [_costs]

    def decision_function(self, X):
        return (X @ self.W_).mean(-1)

    def predict(self, X):
        return self.classes_[(X @ self.W_).mean(-1).argmax(0)]


class MTFLClassifier(BaseBinaryMTFL, ClassifierMixin):
    """Classifier based on MTFL. Code adapted from
    https://github.com/argyriou/multi_task_learning

    Parameters
    ----------
    gamma: float
        Gamma value.
    eps_init: float
        Initial value for epsilon.
    n_iters: int
        Number of iterations per step.
    loss: str
        Loss to use.
    aggregate: str
        Method of aggregation. One of "logistic", "weighted",
        "unweighted".
    """

    def __init__(
        self,
        gamma: float = 1,
        epsilon: float = 1e-4,
        n_iters: int = 10,
        loss: str = "svm",
        aggregate: str = "weighted",
    ):
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_iters = n_iters
        self.loss = loss
        self.aggregate = aggregate

    def fit(self, X, y, tasks):
        if len(np.unique(y)) > 2:
            raise ValueError("`y` should have only two classes")
        y = y.copy()
        y[y == 0] = -1
        self._fit_feat(X, y, tasks)
        if self.aggregate == "logistic":
            self.logistic_ = LogisticRegression(penalty="none")
            self.logistic_.fit(super().predict(X), y)
        return self

    def decision_function(self, X):
        preds = super().predict(X)
        if self.aggregate == "logistic":
            return self.logistic_.decision_function(preds)
        return preds.mean(-1)

    def predict(self, X):
        preds = super().predict(X)
        if self.aggregate == "logistic":
            preds = self.logistic_.predict(preds)
        elif self.aggregate == "weighted":
            preds = np.sign(preds.mean(-1))
        elif self.aggregate == "unweighted":
            preds = np.sign(np.sign(preds).mean(-1))
        preds[preds == -1] = 0
        return preds
