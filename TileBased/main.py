import pygame
import pyscroll
from pytmx import load_pygame, TiledTileLayer


global image

## Initialize Pygame Stuff
pygame.init()
screenWidth = 1200
screenHeight = 600

screen = pygame.display.set_mode((screenWidth, screenHeight))

tmxdata = load_pygame("UndergroundLava.tmx")
width = tmxdata.width * tmxdata.tilewidth
height = tmxdata.height * tmxdata.tileheight

ti = tmxdata.get_tile_image_by_gid
for layer in tmxdata.visible_layers:
    if isinstance(layer, TiledTileLayer):
        for x, y, gid, in layer:
            tile = ti(gid)
            if tile:
                image = tmxdata.get_tile_image(x, y, layer)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(image, [0,0])

    