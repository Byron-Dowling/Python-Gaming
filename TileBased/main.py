import pygame
import pytmx
import sys


pygame.init()

# Set the position of the camera
camera_x = 0
camera_y = 0

# Display a portion of the map surface
screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the TMX file
tmx_data = pytmx.util_pygame.load_pygame("Platformer assets pack\Lava.tmx")

# Create a Pygame surface with the same dimensions as the map
map_surface = pygame.Surface((tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight))

# Iterate over all the layers in the map
for layer in tmx_data.layers:
    # Iterate over all the tiles in the layer
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
    screen.blit(map_surface, (0, 0), pygame.Rect(camera_x, camera_y, screen_width, screen_height))
    
    # Update the screen
    pygame.display.flip()
