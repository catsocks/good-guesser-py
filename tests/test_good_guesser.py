import numpy as np
import pytest

import good_guesser


@pytest.mark.parametrize(
    "test_input,expected",
    (
        (([[1, 4], [2, 6], [3, 12]], [1, 2, 8]), [-2.5, -1.5, 1.25]),
        (([[1, 4], [2, 6]], [7, 3]), [0]),
        (([], []), [0]),
        (([[373, 1, 0], [423, 4, 0], [741, 13, 0], [463, 11, 0]], [4, 6, 14, 10]), [0]),
        # FIXME(catsocks): Test fails with the following parameters.
        # good-guesser.good-guesser=> (multiple-regression [[423 4] [646 5]] [8 8])
        # [0]
        (([[423, 4], [646, 5]], [8, 8]), [0]),
    ),
)
def test_multiple_regression(test_input, expected):
    assert np.allclose(good_guesser.multiple_regression(*test_input), expected)


@pytest.mark.parametrize(
    "test_input,expected",
    (
        (np.array([]), np.zeros((0, 2))),
        (np.array([[1], [2]]), [[1, 1], [1, 2]]),
    ),
)
def test_add_bias(test_input, expected):
    assert np.array_equal(good_guesser.add_bias(test_input), expected)


def test_normal_equation():
    assert np.allclose(
        good_guesser.normal_equation(np.array([[1, 1], [1, 2], [1, 3]]), [3, 2, 4]),
        [2, 0.5],
    )


def test_estimate():
    assert good_guesser.estimate([1.257, 0.004, 0.226], [278, 7]) == pytest.approx(
        3.95, 0.001
    )
