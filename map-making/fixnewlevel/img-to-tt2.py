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

rgb2chan = dict([(y, [(x >> 3) & 0x1, (x >> 2) & 0x1, (x >> 1) & 0x1, x& 0x1]) for (x,y) in colormap.items()])
print(rgb2chan)

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

def imgTott2(imgfn, outfn):
    im = Image.open(imgfn).convert("RGB")
    width, height = im.size
    tilew = width / 16
    tileh = height / 16

    with open(outfn, "wb") as fp:
        fp.write("\x00\x00\x00\x00") # header...
        for ty in range(tileh):
            for tx in range(tilew):
                # now inside the texture tile
                r = []
                g = []
                b = []
                l = []
                for y in range(16):
                    for x in range(16):
                        px = tx * 16 + x
                        py = ty * 16 + y
                        rgb = im.getpixel( (px, py) )
                        chans = rgb2chan[rgb]
                        r += [chans[0]]
                        g += [chans[1]]
                        b += [chans[2]]
                        l += [chans[3]]
                # now convert bitstreams to bytes

                out = ""
                for s in [b,g,r,l]:
                    for bchunk in chunks(s, 8):
                        out += chr(int("".join(["{}".format(i) for i in bchunk]), 2))
                fp.write(out)

imgTott2(sys.argv[1], sys.argv[2])

