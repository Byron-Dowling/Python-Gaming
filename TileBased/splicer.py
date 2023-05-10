"""
    Name:  Byron Dowling
    Class: 5443 2D Python Gaming

    Description:
        - Program is used to crop and derive the sprites from a single
          sprite sheet into multiple individual images.
"""

from PIL import Image
from os import mkdir

#mkdir("Sprites/Idle")
sheet = Image.open("Archaeologist Sprite Sheet.png")
count = 0

width, height = sheet.size

print(f'Height: {height}, Width: {width}')

strideLength = width/8

left = 0
right = strideLength
top = height - 160
bottom = height - 128

for x in range(8):
    icon = sheet.crop((left, top, right, bottom))
    icon.save("Sprites/Roll/{}.png".format(count))
    count += 1
    right = right + strideLength
    left += strideLength