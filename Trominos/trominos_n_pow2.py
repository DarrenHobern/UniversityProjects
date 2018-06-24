"""
Darren Hobern
COMP361
Assignment 1
2017
"""

from trominos_helpers import *

def tile_n_pow2(n, missing, origin=(0,0), tabs=0):
    """
    ARGS:
        n: size of the (sub)board
        missing: missing tile location
        origin: centre of the (sub)board
        tabs: indentation for recursion depth
    """

    if n is 2:
        # The board is a right tromino T
        # Tile with T
        relative_location = tuple([missing[i]-origin[i] for i in range(2)])
        orientation = Orientation(relative_location)
        real_location = tuple([missing[i] + int(not orientation.value[i]) for i in range(2)])

        place_tromino(orientation, real_location[0], real_location[1], tabs)

        # print("{}{} {}".format('  '*tabs, real_location, orientation.name))
        return

    # divide the board into n/2 x n/2 subboards
    n = n//2  # integer division
    # calculate  new offset, aka, centre of subboard split
    # c = tuple([i+n*(o if o is not 0 else 1) for i in c])
    centre = tuple([i+n for i in origin])

    print("{0}Board size is {1}\n{0}Splitting board at {2}.".format('  '*tabs, n*2, centre))

    # find where the missing tile is relative to the centre
    mA, mB, mC, mD = find_missing(centre, missing, tabs=tabs)
    origin_a, origin_b, origin_c, origin_d = find_origins(n, origin)

    print("\n%sSub-board A:" % ('  '*tabs))
    tile_n_pow2(n, mA, origin=origin_a, tabs=tabs+1)

    print("\n%sSub-board B:" % ('  '*tabs))
    tile_n_pow2(n, mB, origin=origin_b, tabs=tabs+1)

    print("\n%sSub-board C:" % ('  '*tabs))
    tile_n_pow2(n, mC, origin=origin_c, tabs=tabs+1)

    print("\n%sSub-board D:" % ('  '*tabs))
    tile_n_pow2(n, mD, origin=origin_d, tabs=tabs+1)
