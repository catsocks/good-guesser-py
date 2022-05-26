from random import randint
import pytest

from examples import num_squares
from good_guesser import good_guesser


@pytest.fixture
def sample_bmp():
    bmp = [
        "               *                                  ",
        "              ***                                 ",
        "             *****                     *          ",
        "            *******                *****          ",
        "           *********            *********         ",
        "          ***********    **   ***********         ",
        "         **************  ****************         ",
        "       ***********************************        ",
        "      ************************************        ",
        "     *************************************        ",
        "     **************************************       ",
        "      *************************************       ",
        "       *************************************      ",
        "        *************************************     ",
        "        **************************************    ",
        "         **************************************   ",
        "         **************************************   ",
        "         ********** ****************************  ",
        "          *******  ****************************** ",
        "          ******   *******************************",
        "          *   *    ****************************** ",
        "                  *****************************   ",
        "                  ****************************    ",
        "                  ***************************     ",
        "                  **************************      ",
        "                     **********************       ",
        "                         *****************        ",
        "                            ****     ****         ",
        "                                      **          ",
        "                                                  ",
    ]
    return [list(row) for row in bmp]


def test_count_pixels(sample_bmp):
    assert num_squares.count_pixels(sample_bmp) == 768


def test_concave_pixels(sample_bmp):
    assert num_squares.concave_pixels(sample_bmp) == 2


# NOTE(catsocks): Adapted from good-guesser.square-grid/run-validation.
def test_good_guesser(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    num_examples = 100
    for _ in range(num_examples):
        square_count = randint(1, 10)
        good_guesser(
            "num-squares-validation",
            num_squares.square_grid(square_count),
            num_squares.count_pixels,
            num_squares.concave_pixels,
            actual_value=square_count,
        )

    results = []
    for _ in range(num_examples):
        square_count = randint(1, 10)
        guess = good_guesser(
            "num-squares-validation",
            num_squares.square_grid(square_count),
            num_squares.count_pixels,
            num_squares.concave_pixels,
        )
        results.append((square_count, max(1, min(10, round(guess)))))

    num_correct_guesses = len([guess for actual, guess in results if actual == guess])
    num_correct_guesses_within_1 = len(
        [guess for actual, guess in results if abs(actual - guess) <= 1]
    )

    assert num_correct_guesses > 20
    assert num_correct_guesses_within_1 > 50

    print(f"Number of correct guesses: {num_correct_guesses}/{num_examples}")
    print(
        "Number of correct guesses with a margin of error of 1: "
        + f"{num_correct_guesses_within_1}/{num_examples}"
    )
