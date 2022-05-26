import ast
import logging
import sys
from numbers import Number
from pathlib import Path

import edn_format
import numpy as np
from more_itertools import chunked

MAX_UNLABELED_EXAMPLES = 20

logger = logging.Logger(__name__, level=logging.INFO)


class GoodGuesserException(Exception):
    """Base good_guesser exception."""


class InvalidInputFuntionError(GoodGuesserException):
    """Raised when an input function returns something other than a number."""


class Example:
    def __init__(self, raw_input, output, labeled):
        self.input = raw_input
        self.output = output
        self.labeled = labeled
        self.visualization = []

    def __eq__(self, other):
        if isinstance(other, Example):
            return (
                self.input == other.input
                and self.output == other.output
                and self.labeled == other.labeled
            )
        return False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self.input!r}, {self.output!r}, {self.labeled!r})"
        )

    def dump(self, file, indent):
        file.write(edn_format.dumps(self.input, indent=2 if indent else None))
        file.write("\n")

        for line in self.visualization:
            file.write(f";; {line}\n")

        if not self.labeled:
            file.write("?")
        file.write(f"{self.output}\n")


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


def good_guesser(
    name,
    raw_input,
    *input_funs,
    actual_value=None,
    preview=False,
    visualizer=None,
):
    path = Path(f"{name}.gg")

    examples = load_examples(path)

    regression = run_regression(input_funs, examples)
    logger.info("New regression: %s", regression)

    # Calculate new guess.
    if actual_value is not None:
        guess = actual_value
    else:
        guess = estimate(regression, apply_inputs(input_funs, raw_input))

    # Calculate old guesses.
    unlabeled = [example for example in examples if not example.labeled]
    for example in unlabeled:
        example.output = estimate(regression, apply_inputs(input_funs, example.input))

    try:
        visited = {example.input for example in examples}
    except TypeError as exc:
        if "unhashable type" in str(exc):
            raise GoodGuesserException("raw input must be hashable") from exc
        raise

    # Add new example.
    under_unlabeled_threshold = len(unlabeled) < MAX_UNLABELED_EXAMPLES
    if (under_unlabeled_threshold and raw_input not in visited) or actual_value:
        examples.append(Example(raw_input, guess, actual_value is not None))

    # Create visualizations.
    if visualizer:
        for example in examples:
            example.visualization = visualizer(example.input, example.output)

    # NOTE(catsocks): Disable indentation when a visualizer is provided because
    # edn_format's indentation can result in some data structures taking an
    # overwhelming amount of space.
    if preview:
        dump_examples(sys.stdout, examples, not visualizer)
    else:
        with path.open("w") as file:
            dump_examples(file, examples, not visualizer)
        logger.info("Wrote examples to file: %s", path)

    return guess


def load_examples(path):
    if not path.exists():
        return []

    try:
        pairs = list(chunked(edn_format.loads_all(path.read_text()), 2, True))
    except ValueError as exc:
        if str(exc) == "iterable is not divisible by n.":
            raise GoodGuesserException(
                "an example is missing either an input or output"
            ) from exc
        raise

    examples = []
    for raw_input, output in pairs:
        is_symbol = isinstance(output, edn_format.Symbol)
        if is_symbol:
            try:
                output = ast.literal_eval(output.name[1:])
            except SyntaxError as exc:
                raise GoodGuesserException(
                    "an example is labeled with an invalid output"
                ) from exc
        examples.append(Example(raw_input, output, not is_symbol))
    return examples


def dump_examples(file, examples, indent):
    for example in examples:
        example.dump(file, indent)


def run_regression(input_funs, examples):
    labeled = [example for example in examples if example.labeled]
    xs_coll = [apply_inputs(input_funs, example.input) for example in labeled]
    y_coll = [example.output for example in labeled]
    return multiple_regression(xs_coll, y_coll)


def apply_inputs(input_funs, raw_input):
    outputs = []
    for fn in input_funs:
        output = fn(raw_input)
        # Prevent np.column_stack from potentially throwing a confusing ValueError in
        # add_bias if an input function returns an object that isn't a number.
        if not isinstance(output, Number):
            unexpected_type = type(output)
            raise InvalidInputFuntionError(
                f"input function {fn} did not return a number"
                + f" (it returned a {unexpected_type} instead)"
            )
        outputs.append(output)
    return outputs
