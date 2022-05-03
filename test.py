import random
import unittest

import example
from square_grid import square_grid


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_bmp_seed = 1651582549
        sample_bmp = [
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
        cls.sample_bmp = [list(row) for row in sample_bmp]


class TestExample(BaseTest):
    def test_count_pixels(self):
        self.assertEqual(example.count_pixels(self.sample_bmp), 768)

    def test_concave_pixels(self):
        self.assertEqual(example.concave_pixels(self.sample_bmp), 2)


class TestSquareGrid(BaseTest):
    def test_square_grid(self):
        self.maxDiff = None
        random.seed(self.sample_bmp_seed)
        self.assertEqual(square_grid(), self.sample_bmp)
