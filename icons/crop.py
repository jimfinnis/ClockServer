#!/usr/bin/env python3 

import sys

"""Crop all images to a bounding box which is the same for every image"""


raise Exception("DO NOT USE THIS - images are cropped individually in convert now.")


from PIL import Image

vals = [1,2,3,4,9,10,11,13,50]

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

def getcrop(name):
    im = Image.open(name)
    im = im.convert('RGB')
    width,height = im.size
    fullsum = getsum(im)
    
    good = 0
    for i in range(0,200):
        im2 = im.crop( (i,i,width-i,height-i))
        sum = getsum(im2)
        print(i,sum)
        if sum==fullsum:
            good = i
        else:
            break
            
    return good
    
def cropfile(name,cropval):
    im = Image.open(name)
    im = im.convert('RGBA')
    width,height = im.size
    im = im.crop((good,good,width-good,height-good))
    im.save(name)
    


# find the minimum preserving cropping margin for all images

good = 20
for i in vals:
    crop = getcrop(f"{i:02}d.png")    
    print(crop)
    crop = getcrop(f"{i:02}n.png")
    print(crop)
    if crop < good:
        good = crop        
        

for i in vals:
    cropfile(f"{i:02}d.png",good)
    cropfile(f"{i:02}n.png",good)
