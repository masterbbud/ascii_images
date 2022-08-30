from PIL import Image, ImageChops

from math import floor


# I dont like pil's convert, so maybe use something else for bw conversion
# 136 tall 56 wide

ax = 56
ay = 136
# might need to set text height (as a ratio height:width)
charstall = 1
maxwidth = 1
path = ''

while True:
    path = input('File path to convert: ')
    try:
        Image.open(path)
    except:
        print('ERROR: Incorrect file path. Try again.')
        continue
    break
while True:
    charstall = input('Height of the resulting image in characters: ')
    try:
        charstall = int(charstall)
        if charstall <= 0:
            raise
    except:
        print('ERROR: Improper value for height. Try again.')
    break
while True:
    maxwidth = input('Max width of the resulting image (ENTER for none): ')
    try:
        if maxwidth == '':
            maxwidth = None
            break
        maxwidth = int(maxwidth)
        if maxwidth <= 0:
            raise
    except:
        print('ERROR: Improper value for max width. Try again.')
    break


print('Loading tilemap...')

img = Image.open('data/Tilemap.png').convert('1')
iw, ih = img.size
charToImg = {}
ct = 32
for y in range(19):
    for x in range(5):
        charToImg[chr(ct)] = img.crop((
            x*ax, y*ay, (x+1)*ax-1, (y+1)*ay-1
        ))
        ct += 1

img = Image.open(path).convert('1')
iw, ih = img.size
charRows = []
charstall = charstall
th = floor(ih / charstall)
tw = floor(th / ay * ax)
for k, v in charToImg.items():
    charToImg[k] = v.resize((tw, th))
    #print(v.size, tw, th)
charswide = floor(iw / tw)
if maxwidth and charswide > maxwidth:
    charswide = maxwidth
    tw = floor(iw / charswide)
    th = floor(tw / ax * ay)
    charstall = floor(ih / th)
print(f'Creating image with size {charswide}x{charstall}')
for row in range(charstall):
    currrow = []
    for col in range(charswide):
        tempimg = img.crop((
            col*tw, row*th, (col+1)*tw, (row+1)*th
        ))
        #print((
        #    col*tw, row*th, (col+1)*tw, (row+1)*th
        #))
        bestTuple = ['', 0]
        for char, possible in charToImg.items():
            #print(tempimg.size, possible.size)
            result = ImageChops.difference(possible, tempimg)
            allList = list(result.getdata())
            ct = allList.count(0)
            if ct > bestTuple[1]:
                bestTuple[0] = char
                bestTuple[1] = ct
        currrow.append(bestTuple[0])
    charRows.append(currrow)
with open('out.txt', 'w') as file:
    for crow in charRows:
        file.write(''.join(crow)+'\n')
print('Wrote to file out.txt')