import sys
from PIL import Image
from copy import deepcopy

def flip_image(p):
    q = Image.new(p.mode, (p.height, p.width))
    for x in range(p.width):
        for y in range(p.height):
            curr = p.getpixel((x, y))
            q.putpixel((y, x), curr)
    print(q.size)
    return q

def aitkinson(img):
    img = deepcopy(img)
    # Aitkinson dithering from http://mike.teczno.com/notes/atkinson.html
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
    return img

orig_img = Image.open(sys.argv[-1]).convert('L')
img = deepcopy(orig_img)
final_img = deepcopy(orig_img)
t_img = flip_image(img)

threshold = 128*[0] + 128*[255]
img = aitkinson(img)
t_img = aitkinson(t_img)

# un-flip
t_img = flip_image(t_img)

# Comparison
for x in range(img.size[0]):
    for y in range(img.size[1]):
        if img.getpixel((x, y)) == t_img.getpixel((x, y)):
            final_img.putpixel((x, y), img.getpixel((x, y)))
        else:
            tallies = [0, 0]  # first is regular, second is transpose
            for pos in [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]:
                if not(pos[0] < 0 or pos[1] < 0 or pos[0] >= img.width or pos[1] >= img.height):
                    diff_norm = abs(orig_img.getpixel(pos) - img.getpixel(pos))
                    diff_transpose = abs(orig_img.getpixel(pos) - t_img.getpixel(pos))
                    if diff_norm < diff_transpose:
                        tallies[0] += 1
                    elif diff_transpose < diff_norm:
                        tallies[1] += 1
            if tallies[0] > tallies[1]:
                final_img.putpixel((x, y), img.getpixel((x, y)))
            else:
                final_img.putpixel((x, y), t_img.getpixel((x, y)))


final_img.show()
