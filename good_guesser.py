import numpy as np

# The next four functions are adapted from the book "Clojure For Data Science" by Henry
# Garner.


def multiple_regression(xs_coll, y_coll):
    assert len(xs_coll) == len(y_coll)
    regression = normal_equation(add_bias(np.array(xs_coll)), y_coll)
    if regression is not None:
        return regression
    return np.array([0])


def add_bias(x):
    """Add a default bias term of 1."""
    return np.column_stack((np.repeat(1, x.shape[0]), x))


def normal_equation(x, y):
    """Return the least-squares solution to a linear matrix equation."""
    xt = x.transpose()
    xtx = np.matmul(xt, x)
    try:
        xtxi = np.linalg.inv(xtx)
    except np.linalg.LinAlgError as exc:
        if str(exc) == "Singular matrix":
            return None
        raise
    xty = np.matmul(xt, y)
    return np.matmul(xty, xtxi)


def estimate(regression, xs):
    """Given a multiple regression, estimate y based on the xs."""
    bias, *more = regression
    return sum(map(lambda x, y: x * y, more, xs), bias)


def good_guesser(name, raw_input, *args, **kwargs):
    pass
