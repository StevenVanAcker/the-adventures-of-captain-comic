#!/usr/bin/env python

import sys

out = "\x80\x00\x0a\x00" # header



for i in range(8):
    out += ("\x00" * 128)

for i in range(128):
    out += chr(i)

out += ("\x4a" * 128)

with open(sys.argv[1], "wb") as fp:
    fp.write(out)
