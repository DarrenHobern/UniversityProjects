#!/usr/bin/python3

"""
Darren Hobern
Assignment 4
COMP361
2017
"""

import math

_DIRECTIONS = { ( 1,2), ( 1,-2), # down rigth right, down left left
                (-1,2), (-1,-2), # up right right, up left left
                ( 2,1), ( 2,-1), # down down right, down down left
                (-2,1), (-2,-1)} # up up right, up up left


def knightstour(boardsize, open_tour):
    """ Complete a knight's tour using slightly optimised brute force.
        ARGS:
            boardsize :: int - width and height of the board
            open_tour :: bool - true if the start and end points can be different
    """

    # Set all points on the board to unvisited
    board = [[False for c in range(boardsize)] for r in range(boardsize)]

    # If it is an open tour search until all points have been visited
    if open_tour:
        return knights_bt(board, [(0,0)], boardsize, open_tour)

    # otherwise we must check that the end point is the same as the start
    else:
        for r in range(math.ceil(boardsize/2)):
            for c in range(r, math.ceil(boardsize/2)):
                print("Starting: {} {}".format(r,c))
                success, route = knights_bt(board, [(r,c)], boardsize, open_tour)
                if success:
                    return success, route
        return False, route


def knights_bt(bd, rt, boardsize, open_tour):
    """ Recursively look for a solution to a knight's tour
        by moving to every possible location and backtracking.
        ARGS:
                bd :: [[Bool]], 2d list representing the board.
                rt :: [(Int,Int)], list of int pairs, showing the current route
                boardsize :: Int, width/height of the board.
                open_tour :: Bool, are we finding an open or closed tour.
    """

    # Clone the route and board, so if the route fails we can safely backtrack.
    route = [p for p in rt]
    board = [[col for col in row] for row in bd]
    final_move = False
    i,j = route[-1]  # Current position is the last cell in the route
    board[i][j] = True  # Mark as visited

    # If we have covered all tiles on the board...
    if len(route) == boardsize*boardsize:
        if open_tour:  # And it's an open tour, we're done.
            return True, route
        else:  # else it's a closed tour, we must check if the start position
               # is adjacent to our current position
            final_move = True

    for dir in _DIRECTIONS:
        di = dir[0] + i
        dj = dir[1] + j
        # Check if we are not moving off the board
        if (0 <= di and di < boardsize and
            0 <= dj and dj < boardsize):

            # Check if we're adjacent to the start position in a closed tour
            if final_move:
                si, sj = route[0]  # Start position is the first cell in the route
                if di == si and dj == sj: # If it is adjacent to the start, end
                    route.append((di,dj))
                    return True, route
            elif board[di][dj] == False:
                success, final_route = knights_bt(board, route+[(di,dj)], boardsize, open_tour)
                # Return the solution
                if success:
                    # Only append the cell if it is part of the route
                    route.append((di,dj))
                    return True, final_route

    return False, None


if __name__ == '__main__':
    print("Wrong file, run using 'python3 knightstour.py'")
