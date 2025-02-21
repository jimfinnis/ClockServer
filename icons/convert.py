#!/usr/bin/env python3 

"""
Convert icons. Does the following for each:

* convert to RGBA 
* work out a cropping margin for the image - how much we can cut off without changing the sum
  of the pixel values
* crop to that size
* convert to rgb565
* output data as C source

To render you'll need to render at x+margin,y+margin and then increment by width.
"""

from PIL import Image

header = """
#if defined(__AVR__)
    #include <avr/pgmspace.h>
#elif defined(__PIC32MX__)
    #define PROGMEM
#elif defined(__arm__)
    #define PROGMEM
#endif

struct icondata {
    unsigned short margin;          // crop margin
    unsigned short cropped_width,cropped_height;
    unsigned short width,height;    // this is BEFORE cropping
    const unsigned short *data;
};

"""

total = 0

def getsum(im):
    width,height = im.size
    pixels = im.load()
    sum = 0
    for y in range(height):
        lst = []
        for x in range(width):
            cpixel = pixels[x, y]
            pixsum = cpixel[0]+cpixel[1]+cpixel[2]
            sum += pixsum
            
    return sum

def getcrop(im):
    width,height = im.size
    fullsum = getsum(im)
    
    margin = 0
    for i in range(0,200):
        im2 = im.crop( (i,i,width-i,height-i))
        sum = getsum(im2)
        if sum==fullsum:
            margin = i
        else:
            break
            
    return margin, im.crop( (margin,margin,width-margin,height-margin) )
    


def convert(file):
    global total
    im = Image.open(file)
    im=im.convert('RGBA')

    origwidth,origheight = im.size    

    # crop the image and record the margin - we'll need to add this to x,y when we render
    margin, im = getcrop(im)
    pixels = im.load()
    width,height = im.size
    total += width*height*2
    
    file = file[:3]
    s = f"const unsigned short _{file}_data[{width*height}] PROGMEM={{\n"

    for y in range(height):
        lst = []
        for x in range(width):
            cpixel = pixels[x, y]
            a = cpixel[3]
            pix = [int((x*a)/255) for x in cpixel[:3]]
            r = pix[0]>>3
            g = pix[1]>>2
            b = pix[2]>>3
            rgb = (r<<11) + (g<<5) + b
            h = f"{rgb:#0{6}x}"
            lst.append(h)
        s += ",".join(lst)+",\n"
        
    s+="};"
    s += f"const struct icondata _{file}= {{ {margin}, {width},{height}, {origwidth},{origheight}, _{file}_data }};\n"
    return s

print(header)
vals = [1,2,3,4,9,10,11,13,50]
for i in vals:
    print(convert(f"{i:02}d.png"))
    print(convert(f"{i:02}n.png"))

print(f"// total size = {total} bytes\n")
    
