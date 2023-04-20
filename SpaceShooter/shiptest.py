"""
    Author:   Byron Dowling, Deangelo Brown, Izzy Olaemimimo
    Class:    5443 2D Python Gaming

    Asset Credits:

        Space Environment Sprites:
            - Author: [FoozleCC]
            - https://foozlecc.itch.io/void-fleet-pack-2
            - https://foozlecc.itch.io/void-environment-pack
            - https://foozlecc.itch.io/void-main-ship 
            - https://norma-2d.itch.io/celestial-objects-pixel-art-pack

"""

import math
import pygame
import pprint
import random
import copy
import os
from PIL import Image, ImageDraw
from random import shuffle
from pygame.math import Vector2
from utilities import load_sprite, load_sprite_rotated, wrap_position
import utilities


UP = Vector2(0, -1)

###################################################################################################
"""
 ██████╗  █████╗  ██████╗██╗  ██╗ ██████╗ ██████╗  ██████╗ ██╗   ██╗███╗   ██╗██████╗ 
 ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔══██╗██╔═══██╗██║   ██║████╗  ██║██╔══██╗
 ██████╔╝███████║██║     █████╔╝ ██║  ███╗██████╔╝██║   ██║██║   ██║██╔██╗ ██║██║  ██║
 ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔══██╗██║   ██║██║   ██║██║╚██╗██║██║  ██║
 ██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ 
                                                                                      
 ██╗███╗   ███╗ █████╗  ██████╗ ███████╗██████╗ ██╗   ██╗                             
 ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝██╔══██╗╚██╗ ██╔╝                             
 ██║██╔████╔██║███████║██║  ███╗█████╗  ██████╔╝ ╚████╔╝                              
 ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  ██╔══██╗  ╚██╔╝                               
 ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗██║  ██║   ██║                                
 ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝                                                                                                          
"""
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, size):

        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = self.getImgWidthHeight(image_file)
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def getImgWidthHeight(self, path):
        """Uses pil to image size in pixels.
        Params:
            path (string) : path to the image
        """
        if os.path.isfile(path):
            im = Image.open(path)
            return im.size
        return None

###################################################################################################
"""
  ██████╗  █████╗ ███╗   ███╗███████╗        
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝        
 ██║  ███╗███████║██╔████╔██║█████╗          
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝          
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗        
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝        
                                             
 ███████╗██████╗ ██████╗ ██╗████████╗███████╗
 ██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝
 ███████╗██████╔╝██████╔╝██║   ██║   █████╗  
 ╚════██║██╔═══╝ ██╔══██╗██║   ██║   ██╔══╝  
 ███████║██║     ██║  ██║██║   ██║   ███████╗
 ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

"""
class GameSprite:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

###################################################################################################
""" 
 ███╗   ███╗██╗███████╗███████╗██╗██╗     ███████╗███████╗
 ████╗ ████║██║██╔════╝██╔════╝██║██║     ██╔════╝██╔════╝
 ██╔████╔██║██║███████╗███████╗██║██║     █████╗  ███████╗
 ██║╚██╔╝██║██║╚════██║╚════██║██║██║     ██╔══╝  ╚════██║
 ██║ ╚═╝ ██║██║███████║███████║██║███████╗███████╗███████║
 ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝╚══════╝╚══════╝╚══════╝
                                                          
"""

class Missiles(GameSprite):
    def __init__(self, location):
        self.Missile_Frames = len(os.listdir("Assets\Sprites\Weapons"))
        self.Missile_Frame = 0
        self.Location = location
        self.FiringInProgress = False
        self.Smoothscale = (100,100)
        self.imageLink = f'Assets\Sprites\Weapons\{self.Missile_Frame}.png'

        self.spriteObject = load_sprite_rotated(self.imageLink, self.Smoothscale, 0)

        super().__init__(self.Location, self.spriteObject, Vector2(0))

    def updateFrames(self):
        if self.Missile_Frame < self.Missile_Frames - 1:
            self.Missile_Frame += 1
            self.imageLink = f'Assets\Sprites\Weapons\{self.Missile_Frame}.png'
            self.spriteObject = load_sprite(self.imageLink, self.Smoothscale)
            self.sprite = self.spriteObject
        else:
            self.Missile_Frame = 0
            self.imageLink = f'Assets\Sprites\Weapons\{self.Missile_Frame}.png'
            self.spriteObject = load_sprite(self.imageLink, self.Smoothscale)
            self.sprite = self.spriteObject
            self.FiringInProgress = False

###################################################################################################
""" 
 ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ ███████╗
 ██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗██╔════╝
 ███████╗███████║██║█████╗  ██║     ██║  ██║███████╗
 ╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║╚════██║
 ███████║██║  ██║██║███████╗███████╗██████╔╝███████║
 ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ ╚══════╝
                                                    
"""
class Shields(GameSprite):
    def __init__(self, location):
        self.Shield_Frames = len(os.listdir("Assets\Sprites\Shields"))
        self.Shield_Frame = 0
        self.Location = location
        self.Smoothscale = (170,170)
        self.imageLink = f'Assets\Sprites\Shields\{self.Shield_Frame}.png'

        self.spriteObject = load_sprite_rotated(self.imageLink, self.Smoothscale, 0)

        super().__init__(self.Location, self.spriteObject, Vector2(0))

    def updateFrames(self):
        if self.Shield_Frame < self.Shield_Frames - 1:
            self.Shield_Frame += 1
            self.imageLink = f'Assets\Sprites\Shields\{self.Shield_Frame}.png'
            self.spriteObject = load_sprite(self.imageLink, self.Smoothscale)
            self.sprite = self.spriteObject
        else:
            self.Shield_Frame = 0
            self.imageLink = f'Assets\Sprites\Shields\{self.Shield_Frame}.png'
            self.spriteObject = load_sprite(self.imageLink, self.Smoothscale)
            self.sprite = self.spriteObject


###################################################################################################
"""
 ███████╗██████╗  █████╗  ██████╗███████╗███████╗██╗  ██╗██╗██████╗ 
 ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██║  ██║██║██╔══██╗
 ███████╗██████╔╝███████║██║     █████╗  ███████╗███████║██║██████╔╝
 ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ 
 ███████║██║     ██║  ██║╚██████╗███████╗███████║██║  ██║██║██║     
 ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     
                                                                    
"""
class Spaceship(GameSprite):
    def __init__(self, smsc):
        self.Idle = True
        self.Thrust = False
        self.Shields = False
        self.RotateLeft = False
        self.RotateRight = False
        self.Firing = False
        self.ShipSmoothscale = smsc
        self.MANEUVERABILITY = 6
        self.ACCELERATION = 0.30
        self.MAX_VELOCITY = 20
        self.ANGLE = 0
        self.direction = Vector2(UP)
        self.Idle_Frames = len(os.listdir("Assets\Sprites\Spaceships\Idle"))
        self.Idle_Frame = 0
        self.ImageLink = f'Assets\Sprites\Spaceships\Idle\{self.Idle_Frame}.png'
        self.ShipSpawnLocations = [(150,350),(600,600),(1000,500),(1500,500),
                                   (1600,700),(900,700),(1500,120),(150,150)]
        self.currentPosition = self.randomLocationSpawn()
        self.SpaceshipShields = Shields(self.currentPosition)
        self.SpaceshipMissiles = Missiles(self.currentPosition)
        self.spriteObject = load_sprite_rotated(self.ImageLink, self.ShipSmoothscale, self.ANGLE)

        GameSprite.__init__(self, self.currentPosition, self.spriteObject, Vector2(0))

    ## Modified Unit Circle Trig Math
    def getUnitCircleQuadrant(self):
        if self.ANGLE >= 0 and self.ANGLE <= 90:
            ## Where X is negative and Y is negative
            self.direction[0] = self.direction[0] * -1
            self.direction[1] = self.direction[1] * -1
        elif self.ANGLE > 90 and self.ANGLE <= 180:
            ## Where X is negative and Y is positve
            self.direction[0] = self.direction[0] * -1
        elif self.ANGLE > 270 and self.ANGLE <= 359:
            ## Where X is positive and Y is negative
            self.direction[1] = self.direction[1] * -1


    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        self.ANGLE += self.MANEUVERABILITY * sign

        if self.ANGLE > 360:
            self.ANGLE -= 360
        elif self.ANGLE < 0:
            self.ANGLE += 360

        ## Rotate by degrees in-place
        self.direction.rotate_ip(self.ANGLE)

        self.direction[0] = abs(self.direction[0])
        self.direction[1] = abs(self.direction[1])

        self.getUnitCircleQuadrant()

        """
            velocity is the padding on the position that moves the ship
        """
        self.velocity = self.direction * self.ACCELERATION

        if clockwise:
            self.spriteObject = load_sprite_rotated(self.ImageLink, 
                                self.ShipSmoothscale, self.ANGLE)
            self.SpaceshipMissiles.spriteObject = load_sprite_rotated(self.SpaceshipMissiles.imageLink, 
                                        self.SpaceshipMissiles.Smoothscale, self.ANGLE)
            self.SpaceshipShields.spriteObject = load_sprite_rotated(self.SpaceshipShields.imageLink,
                                        self.SpaceshipShields.Smoothscale, self.ANGLE)
        else:
            self.spriteObject = load_sprite_rotated(self.ImageLink, 
                            self.ShipSmoothscale, self.ANGLE)
            self.SpaceshipMissiles.spriteObject = load_sprite_rotated(self.SpaceshipMissiles.imageLink, 
                                        self.SpaceshipMissiles.Smoothscale, self.ANGLE)
            self.SpaceshipShields.spriteObject = load_sprite_rotated(self.SpaceshipShields.imageLink,
                                        self.SpaceshipShields.Smoothscale, self.ANGLE)
            
        self.sprite = self.spriteObject
        self.SpaceshipMissiles.sprite = self.SpaceshipMissiles.spriteObject
        self.SpaceshipShields.sprite = self.SpaceshipShields.spriteObject

    def accelerate(self):
        if self.velocity.length() < self.MAX_VELOCITY:
            self.velocity += self.direction * self.ACCELERATION

    def randomLocationSpawn(self):
        shuffle(self.ShipSpawnLocations)
        selection = []
        selection.append(self.ShipSpawnLocations[0])
        print(selection[0])
        return selection[0]
    
    def updateFrames(self):
        if self.Idle_Frame < self.Idle_Frames - 1:
            self.Idle_Frame += 1
        else:
            self.Idle_Frame = 0

    def updateSpaceshipSpriteImage(self):
        if self.Idle:
            self.ImageLink = f'Assets\Sprites\Spaceships\Idle\{self.Idle_Frame}.png'
            self.spriteObject = load_sprite_rotated(self.ImageLink, self.ShipSmoothscale, self.ANGLE)

        elif self.Thrust:
            self.ImageLink = r'Assets\Sprites\Spaceships\Idle\1.png'
            self.spriteObject = load_sprite_rotated(self.ImageLink, self.ShipSmoothscale, self.ANGLE)

        ## Invoking the gamesprite member variable
        self.sprite = self.spriteObject

    def updateSpaceshipLocation(self):
        self.currentPosition = self.position
        self.SpaceshipShields.position = self.currentPosition
        self.SpaceshipMissiles.position = self.currentPosition


###################################################################################################
""" 
  ██████╗  █████╗ ███╗   ███╗███████╗                                                 
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝                                                 
 ██║  ███╗███████║██╔████╔██║█████╗                                                   
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝                                                   
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗                                                 
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝                                                 
                                                                                      
  ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗     ██╗     ███████╗██████╗ 
 ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║     ██║     ██╔════╝██╔══██╗
 ██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║     ██║     █████╗  ██████╔╝
 ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║     ██║     ██╔══╝  ██╔══██╗
 ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗███████╗███████╗██║  ██║
  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                                                      
"""
class GameController:
    def __init__(self, width, height):
        self.Running = True
        self.screenWidth = width
        self.screenHeight = height
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.BG_Frames = len(os.listdir("Assets/Background/Stars"))
        self.BG_Frame = 0
        self.RS_Frames = len(os.listdir("Assets/Background/RotaryStar"))
        self.RS_Frame = 0
        self.BH_Frames = len(os.listdir("Assets/Background/BH"))
        self.BH_Frame = 0
        self.Default_Smoothscale_Dimensions = (200,200)
        self.Spaceship_Smoothscale = (80,80)
        self.FORWARD_ACCELEARATION = 20

    def getScreenSize(self):
        dimensions = (self.screenWidth, self.screenHeight)
        return dimensions
    
    def updateFrames(self):
        if self.BG_Frame < self.BG_Frames - 1:
            self.BG_Frame += 1
        else:
            self.BG_Frame = 0

        if self.RS_Frame < self.RS_Frames - 1:
            self.RS_Frame += 1
        else:
            self.RS_Frame = 0

        if self.BH_Frame < self.BH_Frames - 1:
            self.BH_Frame += 1
        else:
            self.BH_Frame = 0
        
###################################################################################################
"""
  ██████╗  █████╗ ███╗   ███╗███████╗                                
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝                                
 ██║  ███╗███████║██╔████╔██║█████╗                                  
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝                                  
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗                                
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝                                
                                                                     
 ██╗   ██╗ █████╗ ██████╗ ██╗ █████╗ ██████╗ ██╗     ███████╗███████╗
 ██║   ██║██╔══██╗██╔══██╗██║██╔══██╗██╔══██╗██║     ██╔════╝██╔════╝
 ██║   ██║███████║██████╔╝██║███████║██████╔╝██║     █████╗  ███████╗
 ╚██╗ ██╔╝██╔══██║██╔══██╗██║██╔══██║██╔══██╗██║     ██╔══╝  ╚════██║
  ╚████╔╝ ██║  ██║██║  ██║██║██║  ██║██████╔╝███████╗███████╗███████║
   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚══════╝                                                                   
 """

## Initialize Pygame Stuff
pygame.init()

## Rough Dimensions of Byron's Monitor
screenWidth = 1750
screenHeight = 900

GC = GameController(screenWidth, screenHeight)
screen = pygame.display.set_mode((GC.screenWidth, GC.screenHeight))

tick = 0

Player1_Spaceship = Spaceship((85,85))

###################################################################################################
"""
  ██████╗  █████╗ ███╗   ███╗███████╗    ██╗      ██████╗  ██████╗ ██████╗ 
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██║     ██╔═══██╗██╔═══██╗██╔══██╗
 ██║  ███╗███████║██╔████╔██║█████╗      ██║     ██║   ██║██║   ██║██████╔╝
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║     ██║   ██║██║   ██║██╔═══╝ 
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ███████╗╚██████╔╝╚██████╔╝██║     
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝                                                                             
"""
## Run the game loop
while GC.Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GC.Running = False
                
    screen.fill((0,0,0))

    ## Background shit
    StarryBackground = Background(f"Assets/Background/Stars/{GC.BG_Frame}.png", [0, 0], (screenWidth, screenHeight))
    GC.screen.blit(StarryBackground.image, StarryBackground.rect)

    RotaryStar1 = Background(f'Assets/Background/RotaryStar/{GC.RS_Frame}.png', [210,500], (100,100))
    GC.screen.blit(RotaryStar1.image, RotaryStar1.rect)

    RotaryStar2 = Background(f'Assets/Background/RotaryStar/{GC.RS_Frame}.png', [1610,110], (100,100))
    GC.screen.blit(RotaryStar2.image, RotaryStar2.rect)

    Blackhole = Background(f'Assets/Background/BH/{GC.BH_Frame}.png', [815,350], (150,150))
    GC.screen.blit(Blackhole.image, Blackhole.rect)

    Player1_Spaceship.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        Player1_Spaceship.rotate(clockwise=True)
    if keys[pygame.K_RIGHT]:
        Player1_Spaceship.rotate(clockwise=False)
    if keys[pygame.K_RSHIFT]:
        if Player1_Spaceship.Shields==False:
            Player1_Spaceship.Shields=True
            Player1_Spaceship.SpaceshipShields.updateFrames()
            Player1_Spaceship.updateSpaceshipLocation()
            Player1_Spaceship.SpaceshipShields.draw(screen)
    if keys[pygame.K_UP]:
        Player1_Spaceship.accelerate()
        Player1_Spaceship.move(screen)
        Player1_Spaceship.updateSpaceshipSpriteImage()
        Player1_Spaceship.updateSpaceshipLocation()


    if tick % 3 == 0:
        GC.updateFrames()
        Player1_Spaceship.updateFrames()
        Player1_Spaceship.updateSpaceshipSpriteImage()

    tick += 1
    Player1_Spaceship.Shields=False

    pygame.display.flip()
###################################################################################################