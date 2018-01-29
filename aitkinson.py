<<<<<<< HEAD
import sys, PIL.Image

img = PIL.Image.open(sys.argv[-1]).convert('L')
=======
import sys
from PIL import Image

img = Image.open(sys.argv[-1]).convert('L')
>>>>>>> 45e79500176ae41eac83eeb183a6f9b5bda5340a

threshold = 128*[0] + 128*[255]

for y in range(img.size[1]):
    for x in range(img.size[0]):

        old = img.getpixel((x, y))
        new = threshold[old]
        err = (old - new) >> 3 # divide by 8
            
        img.putpixel((x, y), new)
        
        for nxy in [(x+1, y), (x+2, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x, y+2)]:
            try:
                img.putpixel(nxy, img.getpixel(nxy) + err)
            except IndexError:
                pass

img.show()
