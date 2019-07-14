#!/usr/bin/env python

import sys

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def levelMap(fn):
    out = []
    data = open(fn, "rb").read()
    out = [[ord(c) for c in x] for x in chunks(data[4:], 128)]
    return out

def fixLevelMap(lm, x0, xsize, y0, ysize):
    # clear out remaining tree trunks
    for c in [69, 70, 74, 75]:#, 81, 82, 88, 89, 94, 95]:
        lm[8][c] = 56 + 40

#    # make the wiped out trees on the right look ok
    lm[0][76] = 40 + 0
    lm[0][77] = 40 + 0
    lm[0][78] = 40 + 31

    lm[1][76] = 40 + 0
    lm[1][77] = 40 + 31
    lm[2][76] = 40 + 0
    lm[2][77] = 40 + 27
    lm[3][76] = 40 + 0
    lm[3][77] = 40 + 27
    lm[4][76] = 40 + 0
    lm[4][77] = 40 + 29

    # erase the entire thing
    for x in range(x0, x0 + xsize + 2):
        for y in range(0, 8):
            lm[y][x] = 40

    counter = 0

    # now inject the new textures
    for y in range(y0, y0 + ysize):
        for x in range(x0, x0 + xsize):
            lm[y][x] = counter
            counter += 1


    return lm

def writeLevelMap(lm, fn):
    with open(fn, "wb") as fp:
        fp.write("\x80\x00\x0a\x00")
        for y in range(10):
            for x in range(128):
                fp.write(chr(lm[y][x]))

part_file_in = sys.argv[1]
part_file_out = sys.argv[2]

xcoord = 64 #int(sys.argv[3])
ycoord = 2 #int(sys.argv[4])

lm = levelMap(part_file_in)
lm = fixLevelMap(lm, xcoord, 10, ycoord, 4)
writeLevelMap(lm, part_file_out)

