from PIL import Image

header = """
#if defined(__AVR__)
    #include <avr/pgmspace.h>
#elif defined(__PIC32MX__)
    #define PROGMEM
#elif defined(__arm__)
    #define PROGMEM
#endif
"""

def convert(file):
    im = Image.open(file)
    im=im.convert('RGBA')
    pixels = im.load()
    width,height = im.size

    file = file[:3]
    s = f"const unsigned short _{file}[{width*height}] PROGMEM={{\n"

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
        
    s+="0x0000 };"
    return s

print(header)
vals = [1,2,3,4,9,10,11,13,50]
for i in vals:
    print(convert(f"{i:02}d.png"))
    print(convert(f"{i:02}n.png"))


    
