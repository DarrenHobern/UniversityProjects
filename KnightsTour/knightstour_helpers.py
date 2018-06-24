"""
Darren Hobern
Assignment 4
COMP361
2017
"""
def rotate_counter_clockwise(route, b_size):
    nroute = []
    for r,c in route:
        nroute.append( ((c*-1)+b_size-1, r) )
    return nroute


def rotate_clockwise(route, b_size):
    nroute = []
    for r,c in route:
        nroute.append( (c, (r*-1)+b_size-1) )
    return nroute


def rotate_flip(route, b_size):
    nroute = []
    for r,c in route:
        nroute.append( (r*-1+b_size-1, c*-1+b_size-1) )
    return nroute


def replace_corner(offset, dimensions, constant):
    """ Retuns the position of the new edge to replace the quadrant one,
        thereby joining the quadrants together.
        ARGS:
            offset :: (int, int) - rows, columns that this quad is offset by.
            dimensions :: (int, int) - height, width of this quad.
            constant :: ((int,int), (int,int)) - the constant containing the
                start point and relative location to the new end point.
    """

    row = abs_index(offset[0], dimensions[0], constant[0][0])
    col = abs_index(offset[1], dimensions[1], constant[0][1])
    return (row + constant[1][0], col + constant[1][1]), row, col


def adjust_offset(adjustment, board):
    """ Adjust the positions of the given board so that it can be merged
        with other boards and still be traversable.
    """

    for r in range(len(board)):
        for c in range(len(board[r])):
            board[r][c] = (board[r][c][0]+adjustment[0],
                           board[r][c][1]+adjustment[1])

    return board


def abs_index(offset, length, index):
    """ Returns the absolute index. The absolute index is the positive index.
        EG. Converts index of [-1] into [5] for a list of size 6.
        ARGS:
            offset :: int - the distance from 0,0
    """

    if index >= 0:
        return index+offset
    return index+offset+length


def route_to_board(route, dimensions):
    """ Converts the given route to a 2d list of pairs containing the next
        move by the knight in this tour.
    """
    height,width = dimensions
    board = [[(0,0) for c in range(width)] for r in range(height)]

    for p in range(len(route)-1):
        crnt = route[p]
        nxt = route[p+1]

        board[crnt[0]][crnt[1]] = nxt

    return board


def board_to_route(board):
    """ Converts the given board to a list of cells in order of visit. """

    boardsize = len(board)*len(board[0])
    start = board[0][0]
    route = [(0,0), start]
    c = board[start[0]][start[1]]

    while True:
        route.append(c)
        if c == (0,0):
            return route
        c = board[c[0]][c[1]]
