from sklearn.linear_model import LassoCV


def Lasso(X, y):

    clf = LassoCV()
    clf.fit(X, y)

    return clf.coef_
