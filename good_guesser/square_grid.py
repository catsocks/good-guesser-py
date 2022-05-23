from itertools import product
from math import cos, pi, sin
from random import randint, random


def square_grid():
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
