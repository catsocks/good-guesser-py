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
    np.testing.assert_allclose(good_guesser.multiple_regression(*test_input), expected)


@pytest.mark.parametrize(
    "test_input,expected",
    (
        (np.array([]), np.zeros((0, 2))),
        (np.array([[1], [2]]), [[1, 1], [1, 2]]),
    ),
)
def test_add_bias(test_input, expected):
    np.testing.assert_array_equal(good_guesser.add_bias(test_input), expected)


def test_normal_equation():
    np.testing.assert_allclose(
        good_guesser.normal_equation(np.array([[1, 1], [1, 2], [1, 3]]), [3, 2, 4]),
        [2, 0.5],
    )


def test_estimate():
    assert good_guesser.estimate([1.257, 0.004, 0.226], [278, 7]) == pytest.approx(
        3.95, 0.001
    )


@pytest.fixture
def sample_examples():
    return '"Unlabeled"\n?1\n"Labeled"\n0\n', [
        good_guesser.Example("Unlabeled", 1, False),
        good_guesser.Example("Labeled", 0, True),
    ]


def test_load_examples(tmp_path, sample_examples):
    path = tmp_path / "test.gg"
    examples_text, examples_list = sample_examples
    path.write_text(examples_text)
    assert good_guesser.load_examples(path) == examples_list


def test_dump_examples(tmp_path, sample_examples):
    path = tmp_path / "test.gg"
    examples_text, examples_list = sample_examples
    with path.open("w") as f:
        good_guesser.dump_examples(f, examples_list, False)
    assert path.read_text() == examples_text


def test_dump_examples_indentation(tmp_path):
    path = tmp_path / "test.gg"
    example = good_guesser.Example([["H", "e", "l", "l", "o"]], 0, False)

    with path.open("w") as f:
        good_guesser.dump_examples(f, [example], False)
    assert path.read_text() == '[["H" "e" "l" "l" "o"]]\n?0\n'

    with path.open("w") as f:
        good_guesser.dump_examples(f, [example], True)
    assert (
        path.read_text()
        == '[\n  [\n    "H"\n    "e"\n    "l"\n    "l"\n    "o"\n  ]\n]\n?0\n'
    )


def test_example_visualizer(tmp_path):
    path = tmp_path / "test.gg"
    example = good_guesser.Example([["H", "e", "l", "l", "o"]], 0, False)
    example.visualization = ["Hello"]
    with open(path, "w") as f:
        example.dump(f, False)
    assert path.read_text() == '[["H" "e" "l" "l" "o"]]\n;; Hello\n?0\n'


def test_run_regression():
    input_funs = (lambda text: text.count("a"),)
    examples = [
        good_guesser.Example("aa", 2, True),
        good_guesser.Example("aaa", 3, True),
    ]
    np.testing.assert_allclose(
        good_guesser.run_regression(input_funs, examples), [0, 1]
    )


def test_apply_inputs_fails_with_invalid_input_fun():
    input_funs = (lambda _: (1, 2),)
    with pytest.raises(good_guesser.InvalidInputFuntionError):
        good_guesser.apply_inputs(input_funs, None)


def test_good_guesser_saves_examples(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    good_guesser.good_guesser("foo", "Hello", lambda txt: txt.count("l"))
    assert (tmp_path / "foo.gg").read_text() == '"Hello"\n?0\n'


def test_good_guesser_preview(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    good_guesser.good_guesser("foo", "Hello", lambda txt: txt.count("l"), preview=True)
    assert not (tmp_path / "foo.gg").exists()


def test_good_guesser_actual_value(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    good_guesser.good_guesser(
        "foo", "Hello", lambda txt: txt.count("l"), actual_value=2
    )
    assert (tmp_path / "foo.gg").read_text() == '"Hello"\n2\n'
