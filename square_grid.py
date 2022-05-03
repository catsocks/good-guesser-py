from itertools import product
from math import cos, pi, sin
from random import randint, random


# Return a square grid with random rotated squares plotted on it.
def square_grid(width=50, height=30, res=20):
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for _ in range(randint(0, 10) + 1):
        size = randint(0, 5) + 2
        x = (1.5 * size) + randint(0, width - (3 * size))
        y = (1.5 * size) + randint(0, height - (3 * size))
        rot = pi * 2 * random()
        dx, dy = sin(rot), cos(rot)
        idx, idy = -dy, dx
        axes_range = [size * (1 / res) * i for i in range(-res, res)]

        for xx, yy in product(axes_range, axes_range):
            grid[int(y + (dy * xx) + (idy * yy))][int(x + (dx * xx) + (idx * yy))] = "*"
    return grid
