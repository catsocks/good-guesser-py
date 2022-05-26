from itertools import product
from math import cos, pi, sin
from random import randint, random

from good_guesser import good_guesser


def num_squares(bmp):
    for row in bmp:
        print("".join(row))
    return good_guesser("num_squares", bmp, count_pixels, concave_pixels)


def count_pixels(bmp):
    return sum([line.count("*") for line in bmp])


def concave_pixels(bmp):
    count = 0
    for rows in zip(bmp, bmp[1:], bmp[2:]):
        triples = list(zip(*rows))
        for k in zip(triples, triples[1:], triples[2:]):
            if k[1][1] == " " and count_pixels(k) > 4:
                count += 1
    return count


def square_grid():
    """Return a square grid with random rotated squares plotted on it."""
    w, h, res = 50, 30, 20
    bmp = [[" " for _ in range(w)] for _ in range(h)]
    for _ in range(randint(0, 10) + 1):
        size = randint(0, 5) + 2
        x = (1.5 * size) + int(random() * (w - (3 * size)))
        y = (1.5 * size) + int(random() * (h - (3 * size)))
        rot = pi * 2 * random()
        dx, dy = sin(rot), cos(rot)
        idx, idy = -dy, dx
        axes_range = [size * (1 / res) * i for i in range(-res, res)]

        for xx, yy in product(axes_range, axes_range):
            row, col = int(y + (dy * xx) + (idy * yy)), int(x + (dx * xx) + (idx * yy))
            bmp[row][col] = "*"
    return bmp


# def square_grid_visualizer(bmp, _):
#     return ["".join(row) for row in bmp]
