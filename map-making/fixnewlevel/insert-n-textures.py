#!/usr/bin/env python

import sys

intxtf = sys.argv[1]
outtxtf = sys.argv[2]
inmapf = sys.argv[3]
outmapf = sys.argv[4]
extra = int(sys.argv[5])

# fix texture file
orig = open(intxtf, "rb").read()
oldlen = (len(orig)-4)/128

with open(outtxtf, "wb") as fp:
    tlen = ord(orig[0])
    fp.write(chr(tlen + extra))
    fp.write(orig[1:4])

    for i in range(extra):
        fp.write("\xff"*32)
        fp.write("\x00"*32)
        fp.write("\x00"*32)
        fp.write("\x00"*32)

    fp.write(orig[4:])

# fix map file
orig = open(inmapf, "rb").read()

with open(outmapf, "wb") as fp:
    fp.write(orig[:4])
    newdata = "".join([chr(ord(x) + extra) for x in orig[4:]])
    fp.write(newdata)


newlen = oldlen + extra

print("old {}, new {}".format(oldlen, newlen))
