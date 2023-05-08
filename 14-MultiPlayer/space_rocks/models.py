from pygame.math import Vector2
from pygame import transform
from pygame import time
from PIL import Image

import random
from utils import get_random_velocity, load_sound, load_sprite, load_sprite_rotated, wrap_position, distance
import math
import os
import pygame

import json

UP = Vector2(0, -1)


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
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

        super().__init__()

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface, missile=False):
        if not missile:
            self.position = wrap_position(self.position + self.velocity, surface)
        else:
            self.position = (self.position + self.velocity)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

###################################################################################################
"""
  █████╗ ███████╗████████╗███████╗██████╗  ██████╗ ██╗██████╗ 
 ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔═══██╗██║██╔══██╗
 ███████║███████╗   ██║   █████╗  ██████╔╝██║   ██║██║██║  ██║
 ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║   ██║██║██║  ██║
 ██║  ██║███████║   ██║   ███████╗██║  ██║╚██████╔╝██║██████╔╝
 ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝ 
                                                              
"""
class Asteroid(GameSprite):
    def __init__(self, location, smsc_dimensions):
        self.IdleImageLink = r"Assets\Sprites\Asteroids\Explosion\0.png"
        self.Explosion_Frames = len(os.listdir("Assets\Sprites\Asteroids\Explosion"))
        self.Explosion_Frame = 0
        self.InOrbit = True
        self.Exploding = False
        self.Smoothscale=smsc_dimensions
        self.spriteObject = load_sprite(self.IdleImageLink, self.Smoothscale)
        self.ANGLE = random.randrange(0, 359, 3)
        self.direction = Vector2(UP)
        self.ACCELERATION = 0.125
        self.MAX_VELOCITY = 2.5

        ## Rotate by degrees in-place
        self.direction.rotate_ip(self.ANGLE)

        self.direction[0] = abs(self.direction[0])
        self.direction[1] = abs(self.direction[1])

        self.getUnitCircleQuadrant()

        GameSprite.__init__(self, location, self.spriteObject, Vector2(self.direction))

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

    def drawAsteroid(self, screen):
        if self.velocity.length() < self.MAX_VELOCITY:
            self.velocity += self.direction * self.ACCELERATION
        GameSprite.draw(self, screen)
        GameSprite.move(self, screen, False)

    def destroy(self):
        imageLink = f"Assets\Sprites\Asteroids\Explosion\{self.Explosion_Frame}.png"
        self.spriteObject = load_sprite(imageLink, self.Smoothscale)
        self.sprite = self.spriteObject

        if self.Explosion_Frame < self.Explosion_Frames - 1:
            self.Explosion_Frame += 1
        else:
            self.InOrbit = False
            self.kill() 


class GameObject:
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
        # print(f"pos: {self.position}")

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 50

    def __init__(self, position, bullet_callback=None, image ="space_ship_40x40.png"):
        self.bullet_callback = bullet_callback
        self.laser_sound = load_sound("fireEffect")
        self.tick = 0
        self.frame = 0
        self.frames = len(os.listdir("Assets\Spaceships\Idle"))
        self.image = f"Assets\Spaceships\Idle\{self.frame}.png"
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        self.ANGLE = 0
        # self.ship_stuff = self.__str__()['ship_image']
        # self.ship_loc = self.__str__()['position']

        super().__init__(position, load_sprite(self.image, (85,85)), Vector2(0))

    def __str__(self):
        """String version of this objects state"""
        attributes = {}
        attributes["ship_image"] = self.image
        attributes["position"] = (self.position.x, self.position.y)
        return json.dumps(attributes)

    def getAttributes(self):
        """Returns the basic attributes needed to set up a copy of this object
        possibly in a multiplayer setting.
        """
        return self.__str__()

    def getLocation(self):
         return tuple(self.position)
    
    def getVelocity(self):
        return self.velocity.x, self.velocity.y

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.ANGLE += self.MANEUVERABILITY * sign

        if self.ANGLE > 360:
            self.ANGLE -= 360
        elif self.ANGLE < 0:
            self.ANGLE += 360

        self.direction.rotate_ip(angle)
        print(f"Rotating to direction: {self.direction} and angle: {self.ANGLE}")

    def accelerate(self, velocity=None):
        if velocity != None:
            self.velocity = Vector2(velocity)
        else:
            self.velocity += self.direction * self.ACCELERATION

    def draw(self, surface):
        if self.tick % 3 == 0:
            if self.frame < self.frames - 1:
                self.frame += 1
                self.image = f"Assets\Spaceships\Idle\{self.frame}.png"
                self.sprite = load_sprite(self.image, (85,85))
            else:
                self.frame = 0
                self.image = f"Assets\Spaceships\Idle\{self.frame}.png"
                self.sprite = load_sprite(self.image, (85,85))
        self.tick += 1
        angle = self.direction.angle_to(UP)
        rotated_surface = transform.rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(tuple(self.position), bullet_velocity, self.ANGLE)
        self.bullet_callback(bullet)
        self.laser_sound.play()


class NPC(Spaceship):
    def __init__(
        self,
        position,
        bullet_callback,
        ship="space_ship5_40x40",
        targets=[],
        other_npcs=None,
    ):
        self.targets = targets
        self.acceleration = 0.10
        self.speed = random.randint(4, 9)
        self.rotation_speed = random.randint(3, 5)
        self.direction = Vector2(0, 1)
        self.prevVelocity = Vector2(0)
        self.last_randrot_direction = None
        self.tracking_velocity = random.uniform(1.70, 3.0)
        self.other_npcs = other_npcs
        self.bullet_callback = bullet_callback

        self.last_shot_time = 0  # clock tick of last shot
        self.shoot_delay = 250  # millisecond delay between shots
        self.max_shots = self.shoot_delay * 4  # max shots in a group or in a row
        self.shot_time_total = 0  # sum of group shots
        self.shoot_window = (
            1100  # max time a group of shots can be grouped before cooldown
        )
        self.shoot_cooldown = 2000  # delay between shout groupings
        self.cooldown = 0

        super().__init__(position, bullet_callback, ship)

    def accelerate(self):
        self.velocity += self.direction * self.acceleration

    def choose_target(self):
        closestDistance = pow(2, 20)
        closestTarget = None
        for target in self.targets:
            d = distance(target.position, self.position)
            if distance(target.position, self.position) < closestDistance:
                closestTarget = target
                closestDistance = d

        self.target = closestTarget

    def rotate(self):
        if self.target is not None:
            target_direction = self.target.position - self.position
            target_angle = math.degrees(
                math.atan2(target_direction.y, target_direction.x)
            )
            # Added this so it would rotate in proper direction
            target_angle *= -1

            diff_angle = (target_angle - self.direction.angle_to(Vector2(0, 0))) % 360

            if diff_angle < 180:
                self.direction.rotate_ip(-min(360 - diff_angle, self.rotation_speed))
            else:
                self.direction.rotate_ip(min(diff_angle, self.rotation_speed))

    def follow_target(self):
        """Always move toward target"""

        closest_npc = pow(2, 20)
        for other in self.other_npcs:
            if other == self:
                continue
            else:
                dis_other = distance(other.position, self.position)
                if dis_other < closest_npc:
                    closest_npc = dis_other
        # print(f"dis_other: {dis_other}")
        if self.target is not None:
            if dis_other < 100:
                direction = self.direction.rotate_ip(min(30, self.rotation_speed))
            else:
                direction = self.direction
                self.velocity = direction * self.tracking_velocity

    # def check_shoot(self):
    #     self.target_distance = distance(self.target.position, self.position)
    #     current_time = time.get_ticks()

    #     if self.target_distance < 300:
    #         time_from_last_shot = current_time - self.last_shot_time
    #         # check if enough time has elapsed to shoot again

    #         if (
    #             time_from_last_shot > self.shoot_delay
    #             and self.cooldown < self.shoot_cooldown
    #         ):
    #             self.shot_time_total += self.shoot_delay
    #             self.last_shot_time = current_time
    #             if self.shot_time_total < self.shoot_window:
    #                 self.shoot()
    #             else:
    #                 self.shot_time_total = 0
    #                 self.cooldown += time_from_last_shot


class Bullet(GameObject):
    def __init__(self, position, velocity, firingAngle):
        """
            load_sprite_rotated(imageLink, smsc, angle, with_alpha=True)
        """
        self.frame = 0
        self.frames = len(os.listdir("Assets\Sprites\Projectile"))
        self.ANGLE = firingAngle
        self.imageLink = f"Assets\Sprites\Projectile\{self.frame}.png"

        print(f"Firing a bullet at {self.ANGLE} degrees.")

        super().__init__(position, load_sprite_rotated(self.imageLink, (100,100), firingAngle), velocity)

        self.tick = 0

    def move(self, surface):
        self.tick += 1
        self.position = self.position + self.velocity

        if self.tick % 3 == 0:

            if self.frame < self.frames - 1:
                self.frame += 1
                self.imageLink = f"Assets\Sprites\Projectile\{self.frame}.png"
            else:
                self.frame = 0
                self.imageLink = f"Assets\Sprites\Projectile\{self.frame}.png"

            load_sprite_rotated(self.imageLink, (100,100), self.ANGLE)
