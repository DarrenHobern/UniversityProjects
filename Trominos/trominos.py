"""
Darren Hobern
COMP361
Assignment 1
2017
"""

import sys
import random
from trominos_helpers import *
from trominos_n_pow2 import tile_n_pow2


def main():
    # A1.py <board size> [x] [y]
    argv = sys.argv
    argc = len(argv)


    if argc < 2:
        print("ERROR: Not enough arguments.\nPlease provide n x y. If x and y are not provided they will be randomised.")
        print("eg:> %s 8 2 3.\nFor an 8x8 board with the missing cell at 2,3" % argv[0])
        sys.exit(1)
    else:
        n = int(argv[1])  # board width and height

    if argc is 2:
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)
    else:
        x = int(argv[2])  # Missing tile x co ordinate
        y = int(argv[3])  # Missing tile y co ordinate

    offset = (0,0)

    if x >= n or x < 0 or y >= n or y < 0:
        print("Missing tile position cannot be greater than n or less than zero")
        sys.exit(1)

    generate_board(n, x, y)  # Initialises the 2d board array

    if is_power2(n):
        tile_n_pow2(n, (x,y))
        print_board(n)
    else:
        print("ERROR: boarsize is required to be a power of 2")



if __name__ == '__main__':
    main()
