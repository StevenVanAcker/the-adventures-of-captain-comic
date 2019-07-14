#!/usr/bin/env python

import sys

out = "\x00\x00\x00\x00" # header

# first block black
for j in range(128):
    out += chr(0)

out += chr(0xff) * 32
out += chr(0x0) * 32
out += chr(0x0) * 32
out += chr(0xf0) * 32


# rest black
for i in range(85):
    for j in range(128):
        out += chr(0)


with open(sys.argv[1], "wb") as fp:
    fp.write(out)
