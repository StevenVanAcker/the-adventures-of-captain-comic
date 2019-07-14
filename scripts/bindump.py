#!/usr/bin/env python3

import sys, binascii

def tobin(x):
    out = bin(x)[2:]
    return ("0000000000" + out)[-8:]

data = open(sys.argv[1], "rb").read()

for (i, c)  in enumerate(data):
    if i % 2 == 0:
        print()
    if i % 32 == 0:
        print()
    print(tobin(c), end="")
