import pygame
from pytmx import load_pygame, TiledTileLayer

#tmxdata = pytmx.TiledMap("UndergroundLava.tmx")

def map_setup():
    global image

    # Getting / Importing the map
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

if __name__ == 'main':
    print("Shenanigans")