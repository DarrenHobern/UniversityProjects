#!/usr/bin/python3
"""
Darren Hobern
Assignment 4
COMP361
2017
"""

from knightstour_helpers import *

"""
Darren Hobern
Assignment 4
COMP361
Panberry Divide and Conquer algorithm

Paper on Panberry's D&C algorithm: https://www.cs.auckland.ac.nz/~mcw/Teaching/320/refs/divide-conquer/knights-tour.pdf
"""

# Odd board sizes
_5x5= [(0,1), (1,3), (3,4), (4,2), (3,0), (1,1), (0,3), (2,4), (4,3), (2,2),
       (1,4), (0,2), (1,0), (3,1), (1,2), (0,4), (2,3), (4,4), (3,2), (4,0),
       (2,1), (3,3), (4,1), (2,0), (0,1)]

_7x7= [(0, 1), (2, 2), (0, 3), (1, 5), (3, 6), (5, 5), (6, 3), (4, 4), (6, 5),
       (4, 6), (2, 5), (0, 6), (1, 4), (0, 2), (1, 0), (3, 1), (2, 3), (4, 2),
       (5, 0), (6, 2), (5, 4), (6, 6), (4, 5), (2, 4), (0, 5), (2, 6), (3, 4),
       (1, 3), (2, 1), (3, 3), (4, 1), (6, 0), (5, 2), (4, 0), (6, 1), (5, 3),
       (3, 2), (1, 1), (3, 0), (5, 1), (4, 3), (6, 4), (5, 6), (3, 5), (1, 6),
       (0, 4), (1, 2), (2, 0), (0, 1)]

_9x9= [(0, 1), (1, 3), (0, 5), (1, 7), (3, 8), (5, 7), (7, 8), (8, 6), (6, 7),
       (8, 8), (7, 6), (6, 8), (8, 7), (7, 5), (8, 3), (7, 1), (5, 0), (3, 1),
       (1, 0), (0, 2), (2, 1), (4, 0), (3, 2), (5, 1), (7, 2), (8, 0), (6, 1),
       (5, 3), (3, 4), (4, 2), (3, 0), (1, 1), (2, 3), (1, 5), (0, 3), (2, 4),
       (3, 6), (4, 4), (6, 3), (8, 4), (6, 5), (4, 6), (5, 4), (3, 5), (5, 6),
       (4, 8), (2, 7), (0, 8), (1, 6), (0, 4), (2, 5), (3, 7), (4, 5), (6, 4),
       (4, 3), (5, 5), (4, 7), (2, 8), (0, 7), (2, 6), (1, 8), (0, 6), (1, 4),
       (2, 2), (4, 1), (6, 2), (7, 0), (8, 2), (7, 4), (6, 6), (5, 8), (7, 7),
       (8, 5), (7, 3), (8, 1), (6, 0), (5, 2), (3, 3), (1, 2), (2, 0), (0, 1)]


# Even board sizes
_6x6 = [(0, 0), (1, 2), (0, 4), (2, 5), (4, 4), (5, 2), (4, 0), (3, 2), (2, 0),
        (0, 1), (1, 3), (0, 5), (2, 4), (4, 5), (5, 3), (4, 1), (3, 3), (5, 4),
        (3, 5), (1, 4), (2, 2), (0, 3), (1, 5), (3, 4), (5, 5), (4, 3), (5, 1),
        (3, 0), (1, 1), (2, 3), (4, 2), (5, 0), (3, 1), (1, 0), (0, 2), (2, 1),
        (0, 0)]

_6x8 = [(0, 0), (1, 2), (2, 0), (0, 1), (1, 3), (0, 5), (1, 7), (3, 6), (5, 7),
        (4, 5), (5, 3), (4, 1), (3, 3), (5, 4), (4, 6), (2, 7), (0, 6), (2, 5),
        (3, 7), (5, 6), (4, 4), (5, 2), (4, 0), (3, 2), (5, 1), (3, 0), (1, 1),
        (0, 3), (2, 4), (1, 6), (0, 4), (2, 3), (1, 5), (0, 7), (2, 6), (4, 7),
        (5, 5), (3, 4), (4, 2), (5, 0), (3, 1), (4, 3), (3, 5), (1, 4), (2, 2),
        (1, 0), (0, 2), (2, 1), (0, 0)]

_8x6 = [(0, 0), (1, 2), (2, 0), (0, 1), (2, 2), (4, 1), (5, 3), (3, 4), (1, 3),
        (0, 5), (2, 4), (4, 3), (5, 5), (7, 4), (6, 2), (7, 0), (5, 1), (3, 2),
        (4, 0), (6, 1), (4, 2), (3, 0), (1, 1), (0, 3), (1, 5), (2, 3), (0, 4),
        (2, 5), (4, 4), (6, 5), (7, 3), (5, 2), (6, 0), (7, 2), (6, 4), (4, 5),
        (3, 3), (1, 4), (3, 5), (5, 4), (7, 5), (6, 3), (7, 1), (5, 0), (3, 1),
        (1, 0), (0, 2), (2, 1), (0, 0)]

_8x8 = [(0, 0), (1, 2), (2, 0), (0, 1), (1, 3), (0, 5), (1, 7), (3, 6), (5, 7),
        (7, 6), (6, 4), (7, 2), (6, 0), (4, 1), (6, 2), (7, 0), (5, 1), (3, 0),
        (1, 1), (0, 3), (1, 5), (0, 7), (2, 6), (4, 7), (6, 6), (7, 4), (5, 5),
        (6, 7), (7, 5), (6, 3), (7, 1), (5, 0), (3, 1), (1, 0), (0, 2), (1, 4),
        (2, 2), (4, 3), (2, 4), (3, 2), (4, 0), (5, 2), (7, 3), (6, 1), (5, 3),
        (4, 5), (3, 7), (1, 6), (0, 4), (2, 3), (3, 5), (2, 7), (0, 6), (2, 5),
        (4, 4), (5, 6), (7, 7), (6, 5), (4, 6), (3, 4), (4, 2), (5, 4), (3, 3),
        (2, 1), (0, 0)]

_8x10= [(0, 0), (1, 2), (0, 4), (1, 6), (0, 8), (2, 9), (1, 7), (0, 9), (2, 8),
        (0, 7), (1, 9), (3, 8), (5, 9), (7, 8), (6, 6), (4, 5), (3, 3), (5, 4),
        (7, 3), (5, 2), (4, 0), (6, 1), (4, 2), (2, 3), (4, 4), (2, 5), (4, 6),
        (6, 5), (5, 3), (3, 4), (1, 3), (3, 2), (2, 0), (0, 1), (2, 2), (4, 1),
        (6, 0), (7, 2), (6, 4), (4, 3), (3, 5), (1, 4), (0, 6), (2, 7), (1, 5),
        (3, 6), (4, 8), (5, 6), (7, 7), (6, 9), (5, 7), (7, 6), (5, 5), (7, 4),
        (6, 2), (7, 0), (5, 1), (3, 0), (1, 1), (0, 3), (2, 4), (0, 5), (2, 6),
        (4, 7), (6, 8), (4, 9), (3, 7), (1, 8), (3, 9), (5, 8), (7, 9), (6, 7),
        (7, 5), (6, 3), (7, 1), (5, 0), (3, 1), (1, 0), (0, 2), (2, 1), (0, 0)]

_10x8= [(0, 0), (1, 2), (2, 0), (0, 1), (1, 3), (0, 5), (1, 7), (3, 6), (5, 7),
        (7, 6), (9, 7), (8, 5), (9, 3), (8, 1), (7, 3), (9, 4), (8, 6), (7, 4),
        (6, 2), (5, 0), (4, 2), (3, 0), (1, 1), (0, 3), (1, 5), (0, 7), (2, 6),
        (4, 7), (5, 5), (6, 7), (7, 5), (9, 6), (7, 7), (6, 5), (8, 4), (6, 3),
        (5, 1), (7, 2), (6, 0), (4, 1), (5, 3), (3, 4), (4, 6), (2, 7), (0, 6),
        (1, 4), (2, 2), (1, 0), (0, 2), (2, 3), (3, 1), (4, 3), (3, 5), (5, 6),
        (6, 4), (5, 2), (4, 4), (3, 2), (2, 4), (1, 6), (0, 4), (2, 5), (3, 7),
        (4, 5), (3, 3), (5, 4), (6, 6), (8, 7), (9, 5), (8, 3), (9, 1), (7, 0),
        (8, 2), (9, 0), (7, 1), (9, 2), (8, 0), (6, 1), (4, 0), (2, 1), (0, 0)]

_10x10=[(0, 0), (1, 2), (0, 4), (1, 6), (0, 8), (2, 9), (1, 7), (0, 9), (2, 8),
        (4, 9), (6, 8), (8, 9), (9, 7), (7, 8), (9, 9), (8, 7), (7, 9), (9, 8),
        (8, 6), (9, 4), (8, 2), (9, 0), (7, 1), (6, 3), (4, 4), (2, 5), (3, 3),
        (5, 4), (6, 2), (4, 1), (5, 3), (7, 4), (6, 6), (4, 5), (2, 6), (4, 7),
        (3, 5), (1, 4), (0, 6), (2, 7), (4, 6), (3, 4), (5, 5), (4, 3), (6, 4),
        (8, 5), (9, 3), (7, 2), (9, 1), (7, 0), (5, 1), (3, 2), (2, 0), (0, 1),
        (1, 3), (0, 5), (2, 4), (3, 6), (4, 8), (6, 7), (5, 9), (3, 8), (1, 9),
        (0, 7), (1, 5), (0, 3), (2, 2), (1, 0), (0, 2), (2, 3), (1, 1), (3, 0),
        (4, 2), (5, 0), (3, 1), (5, 2), (6, 0), (8, 1), (7, 3), (6, 5), (5, 7),
        (7, 6), (9, 5), (8, 3), (7, 5), (5, 6), (3, 7), (1, 8), (3, 9), (5, 8),
        (7, 7), (6, 9), (8, 8), (9, 6), (8, 4), (9, 2), (8, 0), (6, 1), (4, 0),
        (2, 1), (0, 0)]

# reversed 10x10
_10r10=[(0, 0), (2, 1), (4, 0), (6, 1), (8, 0), (9, 2), (7, 1), (9, 0), (8, 2),
        (9, 4), (8, 6), (9, 8), (7, 9), (8, 7), (9, 9), (7, 8), (9, 7), (8, 9),
        (6, 8), (4, 9), (2, 8), (0, 9), (1, 7), (3, 6), (5, 5), (4, 3), (2, 2),
        (0, 1), (2, 0), (4, 1), (6, 2), (5, 4), (3, 5), (2, 3), (4, 2), (5, 0),
        (3, 1), (1, 0), (0, 2), (1, 4), (3, 3), (5, 2), (7, 3), (8, 1), (6, 0),
        (7, 2), (6, 4), (4, 5), (2, 4), (3, 2), (5, 3), (7, 4), (9, 3), (8, 5),
        (6, 6), (4, 7), (2, 6), (0, 5), (1, 3), (3, 4), (4, 6), (2, 7), (0, 6),
        (2, 5), (4, 4), (6, 3), (7, 5), (5, 6), (3, 7), (1, 8), (3, 9), (5, 8),
        (7, 7), (9, 6), (8, 4), (6, 5), (5, 7), (7, 6), (9, 5), (8, 3), (9, 1),
        (7, 0), (5, 1), (3, 0), (1, 1), (0, 3), (1, 5), (0, 7), (1, 9), (3, 8),
        (5, 9), (6, 7), (8, 8), (6, 9), (4, 8), (2, 9), (0, 8), (1, 6), (0, 4),
        (1, 2), (0, 0)]

_10x12=[(0, 0), (1, 2), (0, 4), (1, 6), (0, 8), (1, 10), (3, 11), (2, 9),
        (1, 11), (0, 9), (2, 10), (0, 11), (1, 9), (0, 7), (2, 8), (3, 10),
        (5, 11), (4, 9), (6, 10), (4, 11), (3, 9), (5, 10), (7, 11), (9, 10),
        (7, 9), (8, 11), (9, 9), (7, 10), (9, 11), (8, 9), (6, 8), (8, 7),
        (9, 5), (8, 3), (9, 1), (7, 0), (5, 1), (3, 0), (1, 1), (0, 3), (1, 5),
        (2, 7), (0, 6), (2, 5), (1, 7), (0, 5), (1, 3), (0, 1), (2, 0), (3, 2),
        (2, 4), (3, 6), (4, 8), (6, 9), (8, 8), (9, 6), (7, 7), (5, 8), (4, 6),
        (6, 7), (7, 5), (6, 3), (4, 4), (6, 5), (8, 4), (7, 6), (9, 7), (7, 8),
        (5, 9), (3, 8), (5, 7), (4, 5), (2, 6), (4, 7), (6, 6), (8, 5), (6, 4),
        (7, 2), (9, 3), (7, 4), (5, 5), (3, 4), (5, 3), (4, 1), (6, 0), (8, 1),
        (7, 3), (5, 2), (3, 3), (1, 4), (2, 2), (1, 0), (0, 2), (2, 3), (4, 2),
        (5, 4), (6, 2), (5, 0), (3, 1), (4, 3), (3, 5), (5, 6), (3, 7), (1, 8),
        (0, 10), (2, 11), (4, 10), (6, 11), (8, 10), (9, 8), (8, 6), (9, 4),
        (8, 2), (9, 0), (7, 1), (9, 2), (8, 0), (6, 1), (4, 0), (2, 1), (0, 0)]

_12x10=[(0, 0), (2, 1), (4, 0), (6, 1), (8, 0), (10, 1), (11, 3), (9, 2),
        (11, 1), (9, 0), (10, 2), (11, 0), (9, 1), (7, 0), (8, 2), (10, 3),
        (11, 5), (9, 4), (10, 6), (11, 4), (9, 3), (10, 5), (11, 7), (10, 9),
        (9, 7), (11, 8), (9, 9), (10, 7), (11, 9), (9, 8), (8, 6), (7, 8),
        (5, 9), (3, 8), (1, 9), (0, 7), (1, 5), (0, 3), (1, 1), (3, 0), (5, 1),
        (7, 2), (6, 0), (5, 2), (7, 1), (5, 0), (3, 1), (1, 0), (0, 2), (2, 3),
        (4, 2), (6, 3), (8, 4), (9, 6), (8, 8), (6, 9), (7, 7), (8, 5), (6, 4),
        (7, 6), (5, 7), (3, 6), (4, 4), (5, 6), (4, 8), (6, 7), (7, 9), (8, 7),
        (9, 5), (8, 3), (7, 5), (5, 4), (6, 2), (7, 4), (6, 6), (5, 8), (4, 6),
        (2, 7), (3, 9), (4, 7), (5, 5), (4, 3), (3, 5), (1, 4), (0, 6), (1, 8),
        (3, 7), (2, 5), (3, 3), (4, 1), (2, 2), (0, 1), (2, 0), (3, 2), (2, 4),
        (4, 5), (2, 6), (0, 5), (1, 3), (3, 4), (5, 3), (6, 5), (7, 3), (8, 1),
        (10, 0), (11, 2), (10, 4), (11, 6), (10, 8), (8, 9), (6, 8), (4, 9),
        (2, 8), (0, 9), (1, 7), (2, 9), (0, 8), (1, 6), (0, 4), (1, 2), (0, 0)]

"""
Board connecting moves, first tuple is the position of the cell to update
second tuple is the relative location.
"""

# Odd board adjustments
_ULedge = ((-3, -1), ( 2,  1)) # the out going point from UL quad
_URcorn = ((-1,  0), ( 2, -1)) # the missing corner for UR quad
_BLedge = (( 0, -3), (-1,  2)) # the out going point from BL quad
_ULcorn = ((-1, -1), ( 1,  2)) # the missing corner for UL quad
_BRedge = (( 2,  0), (-2, -1)) # outgoing point BR
_BLcorn = (( 0, -1), (-2,  1)) # missing corner BL
_URedge = ((-1,  2), ( 1, -2)) # outgoing point UR
_BRcorn = (( 0,  0), (-1, -2)) # missing corner BR

# Even boards adjustments
_sA  = ((-2, -1), (-1,  2))
_sB  = ((-1,  0), ( 1,  2))
_sC  = (( 1,  0), ( 1, -2))
_sD  = (( 0, -1), (-1, -2))


def knightstour(boardsize, open_tour):
    """ Complete a closed knight's tour using Ian Panberry's divide and
        conquer algorithm.
    """

    # First check if the boardsize is one of our predetermined solutions
    if boardsize == 6:
        return _6x6
    elif boardsize == 8:
        return _8x8
    elif boardsize == 10:
        return _10x10

    return knights_bt((boardsize, boardsize))[0]  # Ignore the dimensions

def knights_bt(dimensions):
    """ Find the closed knights tour recursively.
        ARGS:
            dimensions :: (int,int) - no. of rows (height), no. of cols (width)
    """

    height, width = dimensions
    # Exit cases for recurive call
    # Odd boards
    if height == 5 and width == 5:
        return _5x5, (5,5)
    elif height == 7 and width == 7:
        return _7x7, (7,7)
    elif height == 9 and width == 9:
        return _9x9, (9,9)
    # Even boards
    elif height == 6:
        if width == 6:
            return _6x6, (6,6)
        elif width == 8:
            return _6x8, (6,8)
    elif height == 8:
        if width == 6:
            return _8x6, (8,6)
        elif width == 8:
            return _8x8, (8,8)
        elif width == 10:
            return _8x10, (8,10)
    elif height == 10:
        if width == 8:
            return _10x8, (10,8)
        elif width == 10:
            return _10x10, (10,10)
        elif width == 12:
            return _10x12, (10,12)
    elif height == 12:
        if width == 10:
            return _12x10, (12,10)


    # Determine if the quadrants must be odd
    isOdd = (width >= 10 and width % 2 == 0 and width % 4 != 0)
    if isOdd:
        print("odd board")

    # Find the position to cut the board into quadrants.
    row_cut, column_cut = find_cuts(width, height, isOdd)

    # Divide the board at the cut points and recurse until we have a fixed solution.
    ul, ul_dim = knights_bt((row_cut, column_cut))
    ur, ur_dim = knights_bt((row_cut, width-column_cut))
    bl, bl_dim = knights_bt((height-row_cut, column_cut))
    br, br_dim = knights_bt((height-row_cut, width-column_cut))

    # Rotate the quadrants
    if isOdd:
        ul = rotate_flip(route=ul, b_size=ul_dim[0])
        ur = rotate_counter_clockwise(route=ur, b_size=ur_dim[0])
        bl = rotate_clockwise(route=bl, b_size=bl_dim[0])
        # br already has the corner hole in the correct position
    elif width == height and width >= 12 and width % 4 == 0:
        ur = rotate_clockwise(route=ur, b_size=bl_dim[0])
        br = rotate_flip(route=br, b_size=br_dim[0])
        bl = rotate_counter_clockwise(route=bl, b_size=bl_dim[0])


    # Merge the quadrants together.
    board = merge(route_to_board(ul, ul_dim),
                  route_to_board(ur, ur_dim),
                  route_to_board(bl, bl_dim),
                  route_to_board(br, br_dim),
                  isOdd)

    return board_to_route(board), (height, width)


def find_cuts(width, height, isOdd):
    """ Returns the index to cut the board as a pair of integers.
        Adjusted for if the board is to be cut into odd or even boards.
        ARGS:
            width :: int - width of the board
            height :: int - height of the board
            isOdd :: bool - after cutting will the quadrants be odd
        doing integer division to ensure things don't horribly explode
    """

    if isOdd:
        return width//2, height//2

    if width % 4 == 0:
        return width//2, height//2
    return (width-2)//2, (height-2)//2


def merge(ul, ur, bl, br, isOdd):
    """ Merges the four quadrants of the board into a single board.
        ARGS:
            ul :: [(int, int)] - board to go into upper left quadrant
            ur :: [(int, int)] - board to go into upper right quadrant
            bl :: [(int, int)] - board to go into bottom left quadrant
            br :: [(int, int)] - board to go into bottom right quadrant
            isOdd :: bool      - are quadrants odd?
    """

    # Adjust the indicies of the boards for when they're merged together.
    # upper left board has no offset
    bl = adjust_offset((len(ul), 0), bl)
    ur = adjust_offset((0, len(ul[0])), ur)
    br = adjust_offset((len(ul), len(ul[0])), br)

    if isOdd:
        # Upper Left
        ul_edge, ul_row_e, ul_col_e = replace_corner(offset=(0, 0),
                                                dimensions=(len(ul), len(ul[0])),
                                                constant=_ULedge)
        ul_corn, ul_row_c, ul_col_c = replace_corner(offset=(0, 0),
                                                dimensions=(len(ul), len(ul[0])),
                                                constant=_ULcorn)
        # Upper Right
        ur_edge, ur_row_e, ur_col_e = replace_corner(offset=(0, len(ul[0])),
                                                dimensions=(len(ur), len(ur[0])),
                                                constant=_URedge)
        ur_corn, ur_row_c, ur_col_c = replace_corner(offset=(0, len(ul[0])),
                                                dimensions=(len(ur), len(ur[0])),
                                                constant=_URcorn)
        # Bottom Left
        bl_edge, bl_row_e, bl_col_e = replace_corner(offset=(len(ul), 0),
                                                dimensions=(len(bl), len(bl[0])),
                                                constant=_BLedge)
        bl_corn, bl_row_c, bl_col_c = replace_corner(offset=(len(ul), 0),
                                                dimensions=(len(bl), len(bl[0])),
                                                constant=_BLcorn)
        # Bottom Right
        br_edge, br_row_e, br_col_e = replace_corner(offset=(len(ur), len(bl[0])),
                                                dimensions=(len(ur), len(ur[0])),
                                                constant=_BRedge)
        br_corn, br_row_c, br_col_c = replace_corner(offset=(len(ur), len(bl[0])),
                                                dimensions=(len(ur), len(ur[0])),
                                                constant=_BRcorn)
    else:
        # UL
        ul_edge, ul_r, ul_c = replace_corner(offset=(0, 0),
                                            dimensions=(len(ul),len(ul[0])),
                                            constant=_sA)
        # UR
        ur_edge, ur_r, ur_c = replace_corner(offset=(0, len(ul[0])),
                                            dimensions=(len(ur),len(ur[0])),
                                            constant=_sB)
        # BL
        bl_edge, bl_r, bl_c = replace_corner(offset=(len(ul), 0),
                                            dimensions=(len(bl),len(bl[0])),
                                            constant=_sD)
        # BR
        br_edge, br_r, br_c = replace_corner(offset=(len(ur), len(bl[0])),
                                            dimensions=(len(br),len(br[0])),
                                            constant=_sC)


    # Join the boards together
    board = []
    # top half
    for row in range(len(ul)):
        board.append(ul[row]+ur[row])
    # bottom half
    for row in range(len(bl)):
        board.append(bl[row]+br[row])

    # Do the actual edge replacement to join the quadrants together
    if isOdd:
        board[ul_row_e][ul_col_e] = ul_edge
        board[ur_row_c][ur_col_c] = ur_corn
        board[bl_row_e][bl_col_e] = bl_edge
        board[ul_row_c][ul_col_c] = ul_corn
        board[br_row_e][br_col_e] = br_edge
        board[bl_row_c][bl_col_c] = bl_corn
        board[ur_row_e][ur_col_e] = ur_edge
        board[br_row_c][br_col_c] = br_corn
    else:
        board[ul_r][ul_c] = ul_edge
        board[ur_r][ur_c] = ur_edge
        board[br_r][br_c] = br_edge
        board[bl_r][bl_c] = bl_edge

    return board


if __name__ == '__main__':
    print("Wrong file, run using 'python3 knightstour.py'")
