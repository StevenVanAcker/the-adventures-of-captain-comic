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

def makeLevelMap(fn, textmap):
    out = []
    data = open(fn, "rb").read()
    im = Image.new('RGB', (128 * 16, 10 * 16))
    imsolid = Image.new('RGB', (128 * 16, 10 * 16))
    for y,d in enumerate(chunks(data[4:], 128)):
        for x, idx in enumerate(d):
            v = textmap[ord(idx)][0]
            issolid = textmap[ord(idx)][1]
            im.paste(v, (x * 16, y * 16))
            if issolid:
                imsolid.paste(solidtexture, (x * 16, y * 16))
            else:
                imsolid.paste(nonsolidtexture, (x * 16, y * 16))

    return im, imsolid

texture_file = sys.argv[1]
part_file = sys.argv[2]
outimg = sys.argv[3]
outsolid = sys.argv[4]

tm = textureMap(texture_file)
im,imsolid = makeLevelMap(part_file, tm)
im.save(outimg)
imsolid.save(outsolid)

