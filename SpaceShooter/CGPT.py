import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the clock
clock = pygame.time.Clock()

# Set up the game variables
player_pos = pygame.Vector2(screen_width/2, screen_height-50)
player_speed = 5
player_img = pygame.image.load(r'Assets\Sprites\Spaceships\Idle\0.png')
enemy_img = pygame.image.load(r'Assets\Sprites\asteroid.png')
enemy_list = []
enemy_speed = 3
enemy_spawn_timer = 100

# Set up the game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos.x > 0:
        player_pos.x -= player_speed
    if keys[pygame.K_RIGHT] and player_pos.x < screen_width - player_img.get_width():
        player_pos.x += player_speed
    if keys[pygame.K_UP] and player_pos.y > 0:
        player_pos.y -= player_speed
    if keys[pygame.K_DOWN] and player_pos.y < screen_height - player_img.get_height():
        player_pos.y += player_speed

    # Spawn enemies
    if enemy_spawn_timer <= 0:
        enemy_list.append([pygame.Vector2(random.randint(0, screen_width), 0)])
        enemy_spawn_timer = 100
    else:
        enemy_spawn_timer -= 1

    # Move enemies and check for collisions
    for enemy in enemy_list:
        enemy[0].y += enemy_speed
        if enemy[0].y > screen_height:
            enemy_list.remove(enemy)
        if (enemy[0].y + enemy_img.get_height() > player_pos.y and 
            enemy[0].y < player_pos.y + player_img.get_height() and 
            enemy[0].x + enemy_img.get_width() > player_pos.x and 
            enemy[0].x < player_pos.x + player_img.get_width()):
            running = False

    # Draw the screen
    screen.fill((0, 0, 0))
    screen.blit(player_img, player_pos)
    for enemy in enemy_list:
        screen.blit(enemy_img, enemy[0])
    pygame.display.flip()

    # Update the clock
    clock.tick(60)

# Clean up Pygame
pygame.quit()
