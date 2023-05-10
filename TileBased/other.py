import pygame
import pytmx
import csv
import sys
from pygame import transform
from pygame.image import load
from playerLoader import PlayerSelector

###################################################################################################
"""
 ██╗██╗     ██╗     ██╗███╗   ██╗ ██████╗ ██╗███████╗       
 ██║██║     ██║     ██║████╗  ██║██╔═══██╗██║██╔════╝       
 ██║██║     ██║     ██║██╔██╗ ██║██║   ██║██║███████╗       
 ██║██║     ██║     ██║██║╚██╗██║██║   ██║██║╚════██║       
 ██║███████╗███████╗██║██║ ╚████║╚██████╔╝██║███████║       
 ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚══════╝       
                                                            
      ██╗ █████╗  ██████╗██╗  ██╗███████╗ ██████╗ ███╗   ██╗
      ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔═══██╗████╗  ██║
      ██║███████║██║     █████╔╝ ███████╗██║   ██║██╔██╗ ██║
 ██   ██║██╔══██║██║     ██╔═██╗ ╚════██║██║   ██║██║╚██╗██║
 ╚█████╔╝██║  ██║╚██████╗██║  ██╗███████║╚██████╔╝██║ ╚████║
  ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
                                                            
"""
class IllinoisJackson:
    def __init__(self, location, smsc_dimensions, inverted=False):

        self.Player = ""
        self.SpriteObject = ""
        temp = PlayerSelector()
        self.Player = temp.player
        self.smsc = smsc_dimensions
        self.player_x = location[0]
        self.player_y = location[1]

        self.idleFrame = 0
        self.idleFrames = self.Player["Action"]["Idle"]["frameCount"]
        self.idleImageLink = self.Player["Action"]["Idle"]["imagePath"] + f"\{self.idleFrame}.png"

        self.SpriteObject = self.load_sprite()


    def load_sprite(self,with_alpha=True):
        loaded_sprite = load(self.idleImageLink)
        loaded_sprite = transform.smoothscale(loaded_sprite, self.smsc)

        if with_alpha:
            return loaded_sprite.convert_alpha()
        else:
            return loaded_sprite.convert()
    
    def updateFrames(self):
        if self.idleFrame < self.idleFrames - 1:
            self.idleFrame += 1
        else:
            self.idleFrame = 0

        self.idleImageLink = self.Player["Action"]["Idle"]["imagePath"] + f"\{self.idleFrame}.png"

        self.SpriteObject = self.load_sprite()

    def movePlayer(self, x=0, y=0):
        self.player_x += x
        self.player_y += y


    def drawPlayer(self, surface):
        blit_position = (self.player_x, self.player_y)
        surface.blit(self.SpriteObject, blit_position)



pygame.init()
tick = 0

# Set the position of the camera
camera_x = 0
camera_y = 460

# Display a portion of the map surface
screen_width = 1500
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

IJ = IllinoisJackson((camera_x + 250, camera_y - 100), (100,100))

# Load the TMX file
tmx_data = pytmx.util_pygame.load_pygame("Platformer assets pack\Level_1.tmx")

# Load the collision layer CSV file
with open("Platformer assets pack\Level_1.csv", "r") as f:
    reader = csv.reader(f)
    collision_data = [[int(cell) for cell in row] for row in reader]

# Create a new layer in the TMX data object for the collision layer
collision_layer = pytmx.TiledObjectGroup(IJ)
collision_layer.name = "Collision"
collision_layer.visible = False
collision_layer.opacity = 1.0
collision_layer.width = tmx_data.width
collision_layer.height = tmx_data.height
collision_layer.tiles = [[None for y in range(tmx_data.height)] for x in range(tmx_data.width)]

# Iterate over the collision layer data and set the corresponding tiles in the collision layer object
for x in range(tmx_data.width):
    for y in range(tmx_data.height):
        gid = collision_data[y][x]
        if gid != 0:
            tile = pytmx.TiledTile()
            tile.gid = gid
            tile.width = tmx_data.tilewidth
            tile.height = tmx_data.tileheight
            collision_layer.tiles[x][y] = tile

# Add the collision layer to the TMX data object
tmx_data.object_groups.append(collision_layer)

# Create a Pygame surface with the same dimensions as the map
map_surface = pygame.Surface((tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight))

# Iterate over all the layers in the map
for layer in tmx_data.layers:
    # If the layer is not the collision layer, iterate over all the tiles in the layer and blit them onto the map surface
    if layer.name != "Collision":
        for x, y, image in layer.tiles():
            # Calculate the position of the tile in pixels
            px = x * tmx_data.tilewidth
            py = y * tmx_data.tileheight

            # Blit the tile onto the map surface
            map_surface.blit(image, (px, py))


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the input from the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= 5
    elif keys[pygame.K_RIGHT]:
        camera_x += 5
    if keys[pygame.K_UP]:
        camera_y -= 5
    elif keys[pygame.K_DOWN]:
        camera_y += 5

    # Clamp the camera position to the bounds of the map
    camera_x = max(0, min(camera_x, tmx_data.width * tmx_data.tilewidth - screen_width))
    camera_y = max(0, min(camera_y, tmx_data.height * tmx_data.tileheight - screen_height))

    # Blit a portion of the map surface onto the screen
    screen.blit(map_surface.subsurface(pygame.Rect(camera_x, camera_y, screen_width, screen_height)), (0, 0))

    # Update the display
    pygame.display.flip()
