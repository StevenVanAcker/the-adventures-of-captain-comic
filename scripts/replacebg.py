#!/usr/bin/env python

import sys
from PIL import Image

# RGBl
colormap = {
        0b0000: (0x00,0x00,0x00),
        0b0010: (0x00,0x00,0xAA),
        0b0100: (0x00,0xAA,0x00),
        0b0110: (0x00,0xAA,0xAA),
        0b1000: (0xAA,0x00,0x00),
        0b1010: (0xAA,0x00,0xAA),
        0b1100: (0xAA,0x55,0x00),
        0b1110: (0xAA,0xAA,0xAA),

        0b0001: (0x55,0x55,0x55),
        0b0011: (0x55,0x55,0xFF),
        0b0101: (0x55,0xFF,0x55),
        0b0111: (0x55,0xFF,0xFF),
        0b1001: (0xFF,0x55,0x55),
        0b1011: (0xFF,0x55,0xFF),
        0b1101: (0xFF,0xFF,0x55),
        0b1111: (0xFF,0xFF,0xFF),
}

solidtexture = Image.new('RGB', (16, 16), color=(255,255,255))
nonsolidtexture = Image.new('RGB', (16, 16))

def img_parseBitsToArray(data):
    out = []
    # the input data is formatted as 4 times 256 bits, representing the blue, green, red and gray bits of a 16x16 image top-left to bottom-right
    bluebits = data[0:32]
    greenbits = data[32:64]
    redbits = data[64:96]
    graybits = data[96:128]

    for i in range(32):
        b = ord(bluebits[i])
        g = ord(greenbits[i])
        r = ord(redbits[i])
        l = ord(graybits[i])

        for ii in range(8):
            bbit = 0x1 & (b >> (7 - ii))
            rbit = 0x1 & (r >> (7 - ii))
            gbit = 0x1 & (g >> (7 - ii))
            lbit = 0x1 & (l >> (7 - ii))

            val = (rbit << 3) | (gbit << 2) | (bbit << 1) | (lbit << 0)
            out += [val]

    return out

def printArr(arr):
    out = ""
    for i,v in enumerate(arr):
        if i > 0 and i % 16 == 0:
            out += "\n"
        out += "{:02x} ".format(v)

    print(out)


def img_getImageFromBytes(data):
    imgdata = img_parseBitsToArray(data)
    im = Image.new('RGB', (16, 16))
    im.putdata([colormap[x] for x in imgdata])
    return im

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def textureMap(fn):
    out = []
    data = open(fn, "rb").read()
    cutoff = ord(data[0])
    for i,d in enumerate(chunks(data[4:], 128)):
        im = img_getImageFromBytes(d)
        # im.save("img{:05d}.png".format(i))
        out += [(im, i > cutoff)]
    return out

def levelMap(fn):
    out = []
    data = open(fn, "rb").read()
    out = [[ord(c) for c in x] for x in chunks(data[4:], 128)]
    return out

def fixLevelMap(lm, x0, xsize, y0, ysize):
    # clear out remaining tree trunks
    for c in [69, 70, 74, 75, 81, 82, 88, 89, 94, 95]:
        lm[8][c] = 56

    # make the wiped out trees on the right look ok
    lm[0][96] = 0
    lm[0][97] = 0
    lm[0][98] = 31

    lm[1][96] = 0
    lm[1][97] = 31
    lm[2][96] = 0
    lm[2][97] = 27
    lm[3][96] = 0
    lm[3][97] = 27
    lm[4][96] = 0
    lm[4][97] = 29

    # erase the entire thing
    for x in range(x0, x0 + xsize):
        for y in range(0, 8):
            lm[y][x] = 0x0

    # add offset to all values
    for x in range(128):
        for y in range(10):
            lm[y][x] += 160


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
                print(y, x, lm[y][x])
                fp.write(chr(lm[y][x]))



def makeLevelMap(fn, textmap):
    out = []
    data = open(fn, "rb").read()
    im = Image.new('RGB', (128 * 16, 10 * 16))
    imsolid = Image.new('RGB', (128 * 16, 10 * 16))
    for y,d in enumerate(chunks(data[4:], 128)):
        bottomvals = list(set(d))
        print("last line vals: {}".format([ord(x) for x in bottomvals]))
        for x, idx in enumerate(d):
            v = textmap[ord(idx)][0]
            issolid = textmap[ord(idx)][1]
            im.paste(v, (x * 16, y * 16))
            if issolid:
                imsolid.paste(solidtexture, (x * 16, y * 16))
            else:
                imsolid.paste(nonsolidtexture, (x * 16, y * 16))

    return im, imsolid

part_file_in = sys.argv[1]
part_file_out = sys.argv[2]

lm = levelMap(part_file_in)
lm = fixLevelMap(lm, 64, 32, 2, 5)
writeLevelMap(lm, part_file_out)

#im_in,imsolid_in = makeLevelMap(part_file_in, tm_in)

# change texture map
# write texture map

# read background image and split into texture files
# add new textures into texture file, change solid offset
# change texture ids in level part



