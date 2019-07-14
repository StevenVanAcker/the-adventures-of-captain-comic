#!/usr/bin/env python

import sys

# read first byte of TT2 file
# ensure all bytes of last layer in PT file are x+1

texturefile = sys.argv[1]
partfile = sys.argv[2]

texturedata = open(texturefile, "rb").read()
texturecount = (len(texturedata) - 4) / 128
cutoff = ord(texturedata[0])

print cutoff

data = open(partfile, "rb").read()

with open(partfile, "wb") as fp:
    sb = 4 + (9 * 128)
    fp.write(data[:sb])
    for b in data[sb:]:
        if ord(b) <= cutoff:
            #fp.write(chr(cutoff + 1))
            fp.write(chr(texturecount))
        else:
            fp.write(b)



