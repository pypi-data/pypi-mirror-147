from sklearn.utils.estimator_checks import check_estimator

from kernel_knockoffs import KernelKnockoffs


def test_estimator_KernelKnockoffs():
    check_estimator(KernelKnockoffs())
