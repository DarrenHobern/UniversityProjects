#!/usr/bin/python3
"""
Darren Hobern
Assignment 4
COMP361
2017
"""
import tkinter as tk
import time
from knightstour_bf import knightstour as kt_bf
from panberry import knightstour as kt_pan


_SIZE = 900 # size of the display

def build_gui(boardsize, route, duration):
    root = tk.Tk()
    canvas = tk.Canvas(root, height=_SIZE,width=_SIZE)
    c_fill = "#333"

    cellsize = _SIZE / boardsize
    # Draw the cells
    for r in range(boardsize):
        for c in range(boardsize):
            x1 = c*cellsize
            y1 = r*cellsize
            x2 = x1+cellsize
            y2 = y1+cellsize
            canvas.create_rectangle(x1, y1, x2, y2, fill=c_fill)

    sy,sx = route[0]  # startX, startY
    for i in range(len(route)-1):
        y,x = route[i]  # Current cell
        ny,nx = route[i+1]  # Next cell
        # Offset by the visual cellsize and centre.
        x = x*cellsize+cellsize/2
        nx = nx*cellsize+cellsize/2
        y = y*cellsize+cellsize/2
        ny = ny*cellsize+cellsize/2

        if boardsize < 32:  # Boards bigger that this make the text impossible to read
            canvas.create_text(x,  y,  fill="white", text=str(i), width=cellsize)
            if sy != route[i+1][0] or sx != route[i+1][1]:
                canvas.create_text(nx, ny, fill="white", text=str(i+1), width=cellsize)
        canvas.create_line(x, y, nx, ny, fill="blue")

    canvas.pack()
    l = tk.Label(root, anchor=tk.S, padx=350, text="Time: {}s".format(duration))
    l.pack()
    root.mainloop()


def invalid_boardsize(boardsize, open_tour, panberry):
    """ Returns True if the boardsize does not have a valid tour.
        Boards are always square.
        Possible boardsizes from: http://gaebler.us/share/Knight_tour.html
        ARGS:
            boardsize :: int - the width and height of the over all board
            open_tour :: bool - the tour can end somewhere other than where it
                                starts.
            panberry :: bool - the algorithm to use is Panberry's D&C
                                Panberry will always produce closed tours.
    """

    # No tours exist for less than 5x5
    if boardsize < 5:
        return True

    if panberry:
        i = boardsize
        while i > 20:
            i = i//2
            if i % 2 != 0:
                print("The required algorithm for this board size has not \
yet been implemented, sorry.")
                return True

    # Open tours can be any boardsize greater than or equal to 5x5
    if open_tour:
        return False
    # Closed tours boardsize must also be even, thereby start at 6x6
    else:
        return (boardsize % 2 != 0 or boardsize < 6)


def main():
    while True:
        boardsize = int(input("Enter the boardsize: "))
        algorithm = input("What algorithm would you like?\n\
1: Brute Force\n2: Parberry\n")
        open_tour = input("Is this a closed tour? Y/n: ")
        open_tour = open_tour.lower() in ["n", "no", "false", "f"]

        if algorithm not in ['1','2']:
            print("Invalid algorithm, should be 1 or 2")
            continue

        if invalid_boardsize(boardsize, open_tour, algorithm == '2'):
            print("Invalid boardsize. Boardsize must be at least 5x5.\n\
Closed tours also require the boardsize to be even.\n")
            continue

        break

    print("Attempting to find a{s_open} knight's tour on a {size}x{size} \
board.".format(s_open="n open" if open_tour else " closed",size=boardsize))

    if algorithm is '1': # Brute force
        if boardsize >= 7:
            print("This could take some time...")

        start_time = time.time()
        success, route = kt_bf(boardsize, open_tour)
        end_time = time.time()
    else: # Panberry divide and conquer
        start_time = time.time()

        route = kt_pan(boardsize, open_tour)
        # Check if we covered all the cells of the board
        success = len(route)-1 == boardsize*boardsize
        end_time = time.time()
    time_difference = end_time - start_time


    route_length = len(route) if open_tour else len(route)-1
    print("{}/{}".format(route_length, boardsize*boardsize))

    print("Was {s_found}successfully able to find a{s_open} knight's tour in \
{s_time}s using {algo} algorithm.".format(s_found="" if success else "un",
            s_open="n open" if open_tour else " closed",
            s_time=round(time_difference, 4),
            algo="a brute force" if algorithm is '1' else "Panberry's Divide & Conquer"))

    build_gui(boardsize, route, round(time_difference,4))


if __name__ == '__main__':
    main()
