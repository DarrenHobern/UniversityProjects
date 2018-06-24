"""
Darren Hobern
COMP361
Assignment 1
2017
"""

from enum import Enum


board = []
# alpha_trom = 'a'

class Orientation(Enum):
    """ Tuples corrospond to the relative location of the missing tile. """
    UL = (1,0)
    UR = (0,0)
    LL = (1,1)
    LR = (0,1)

class Tromino(Enum):
    """ Tuple locations of the two lines that are removed to make up the tromino. """
    """ Relative location within the board array of the lines that need to be removed. """

    UL = ((2,1), (1,1))
    UR = ((2,1), (3,1))
    LL = ((1,1), (2,0))
    LR = ((2,0), (3,1))

class Subboard(Enum):
    """ Translation applied to the centre of the board to find the subboards.
    """
    A = (-1, 0)   # Top left
    B = (0, 0)    # Top right
    C = (-1, -1)  # Bottom left
    D = (0, -1)   # Bottom right


def find_missing(centre, missing, tabs=0):
    """
    ARGS:
        centre :: (int, int), centre of the split
        missing :: (int, int), the missing square
    """

    mA = [sum(x) for x in zip(Subboard.A.value, centre)]
    mB = [sum(x) for x in zip(Subboard.B.value, centre)]
    mC = [sum(x) for x in zip(Subboard.C.value, centre)]
    mD = [sum(x) for x in zip(Subboard.D.value, centre)]

    if missing[0] < centre[0] and missing[1] >= centre[1]:     # A
        tromino = Orientation.LR
        mA = tuple(missing)
    elif missing[0] >= centre[0] and missing[1] >= centre[1]:  # B
        tromino = Orientation.LL
        mB = tuple(missing)
    elif missing[0] < centre[0] and missing[1] < centre[1]:    # C
        tromino = Orientation.UR
        mC = tuple(missing)
    elif missing[0] >= centre[0] and missing[1] < centre[1]:   # D
        tromino = Orientation.UL
        mD = tuple(missing)
    else:
        print("Something went wrong finding the missing tiles")

    place_tromino(tromino, centre[0], centre[1], tabs=tabs)

    return mA, mB, mC, mD


def find_origins(n, centre):
    """
    ARGS:
        n :: int, board size
        centre :: (int, int) centre of the current split

    Finds the bottom left corner of the new subboards
    """

    origin_a = tuple([centre[i]+n+n*Subboard.A.value[i] for i in range(2)])
    origin_b = tuple([centre[i]+n+n*Subboard.B.value[i] for i in range(2)])
    origin_c = tuple([centre[i]+n+n*Subboard.C.value[i] for i in range(2)])
    origin_d = tuple([centre[i]+n+n*Subboard.D.value[i] for i in range(2)])

    return origin_a, origin_b, origin_c, origin_d


def is_power2(num):
    """
    States if a number is a power of two.
    Code from: http://code.activestate.com/recipes/577514-chek-if-a-number-is-a-power-of-two/
    """
    return (num != 0 and ((num & (num - 1)) == 0))


def is_odd(num):
    """
    Returns true if:
        num is odd,
        num > 5
        (num^2 -1) % 3 == 0
    """

    return (num % 2 != 0 and num > 5 and (pow(num,2)-1) % 3 == 0)


def is_even(num):
    """
    Returns true if:
        num is even,
        num > 8
        (num^2 -1) % 3 == 0
    """

    return (num % 2 == 0 and num > 8 and (pow(num,2)-1) % 3 == 0)


def generate_board(n, x, y):
    """ Builds the array representing the board. """

    global board

    board = [[' ' for i in range(2*n+1)] for j in range(n+1)]

    for r in range(len(board)):
        for c in range(len(board[r])):
            if r is len(board)-1:
                if c % 2 != 0:
                    board[r][c] = '_'
            else:
                if c % 2 == 0:
                    board[r][c] = '|'
                else:
                    board[r][c] = '_'

    board[y][2*x+1] = '#'


def print_board(n):
    """ Prints the board in reverse order to invert the y axis.
        Making (0,0) the bottom left corner.
    """

    for row in reversed(board):
        print(''.join(row))


def place_tromino(orientation, x, y, tabs=0):
    """ Places a tromino on the board at the given location with the given
        orientation.
    """

    print("{}{} {}".format('  '*tabs, (x, y), orientation.name))
    for t in Tromino[Orientation(orientation).name].value:
        board[y-1+t[1]][(2*x-1)+t[0]-1] = ' '
