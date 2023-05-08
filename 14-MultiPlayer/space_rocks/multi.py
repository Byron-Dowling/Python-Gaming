import pygame

from models import Asteroid, Spaceship, NPC, Background
from utils import get_random_position, load_sprite, print_text, load_sound
from random import shuffle
import ast
import messenger

import pygame
import math
import random
from pygame.math import Vector2
import sys
import os


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self, multiplayer=None):
        self._init_pygame()
        self.width = 1500
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height))

        ## Background Stuff
        self.tick = 0
        self.BG_Frames = len(os.listdir("Assets/Background/Stars"))
        self.BG_Frame = 0
        self.RS_Frames = len(os.listdir("Assets/Background/RotaryStar"))
        self.RS_Frame = 0
        self.BH_Frames = len(os.listdir("Assets/Background/BH"))
        self.BH_Frame = 0

        ## Asteroid Stuff
        self.Locations = [(100,150),(300,300),(800,400),(1300,200),
                                   (1100,600),(700,700),(1500,620),(650,450),
                                   (1700,850),(800,800),(100,620),(150,450),
                                   (1700,100),(100,800),(1100,120),(150,1000)]
        
        self.ASTEROID_COUNT = len(self.Locations)
        self.explosion = load_sound("explosion")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.__host = False

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship(
            (self.width // 2, self.height // 2), self.bullets.append
        )
        self.__messenger = multiplayer


        if multiplayer != None:
            self.__messenger.setCallback(self.__receiveMessage)

            self.__sendMessage(
                {'Type': 'Who'}
            )

            self.__sendMessage(
                {'Type': 'Join',
                 'Message': self.__messenger.user + ' has joined the game!',
                 'Ship': [self.spaceship.getLocation()]
                 }
            )
            self.__playerIds = []

        self.__otherPlayers = []
        self.__allPlayers = [self.spaceship]

        self.npcs = []

        self.started = False

        # self.npcs.append(
        #     NPC(
        #         (self.width * 0.05, self.height * 0.05),
        #         self.bullets.append,
        #         "space_ship5_40x40",
        #         [self.spaceship],
        #         other_npcs=self.npcs,
        #     )
        # )

        # self.npcs.append(
        #     NPC(
        #         (self.width * 0.95, self.height * 0.95),
        #         self.bullets.append,
        #         "space_ship6_40x40",
        #         [self.spaceship],
        #         other_npcs=self.npcs,
        #     )
        # )

        for index, item in enumerate(self.Locations):
            self.asteroids.append(Asteroid(item, (150,150)))

    def other_npcs(self):
        return self.npcs
    

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


    def main_loop(self):
        while True:
            self._handle_input()
            if self.started:
                self._process_game_logic()
            self._draw()

            if self.tick % 3 == 0:
                self.updateFrames()
            self.tick += 1
            

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):

        sendMessage = False
        Message = {
            'Type': 'Event',
            'Events': []
        }

        for event in pygame.event.get():
            #self.started = True
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()
                sendMessage = True
                Message['Events'].append({'Type': 'Shoot'})
                
            if event.type == pygame.KEYUP:
                print("key released send message")

        is_key_pressed = pygame.key.get_pressed()
        
        

        if not self.started:
            if is_key_pressed[pygame.K_g]:
                self.started = True

        if self.spaceship:
            # print(f"velocity: {self.spaceship.velocity}")
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
                sendMessage = True
                Message['Events'].append({'Type': 'Rotate', 'Clockwise': 1})
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
                sendMessage = True
                Message['Events'].append({'Type': 'Rotate', 'Clockwise': 0})
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
                sendMessage = True
                Message['Events'].append({'Type': 'Accelerate'})
                if len(self.npcs) > 0:
                    for npc in self.npcs:
                        npc.accelerate()
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.accelerate(0)
                sendMessage = True
                Message['Events'].append({'Type': 'Stop'})

            if sendMessage == True:
                self.__sendMessage(Message)

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            #print(game_object)
            game_object.move(self.screen)

        ## Not sure we care about spaceship asteroid collisions
        # if self.spaceship:
        #     for asteroid in self.asteroids:
        #         if asteroid.collides_with(self.spaceship):
        #             self.spaceship = None
        #             self.message = "You lost!"
        #             break

        if len(self.npcs) > 0:
            for npc in self.npcs:
                npc.choose_target()
                npc.rotate()
                npc.follow_target()
                # npc.check_shoot()

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.Exploding == False:
                    if asteroid.collides_with(bullet):
                        self.ASTEROID_COUNT -= 1
                        asteroid.Exploding = True
                        self.explosion.play()
                        self.bullets.remove(bullet)
                        break

        for asteroid in self.asteroids[:]:
            if asteroid.InOrbit:
                if asteroid.Exploding:
                    asteroid.destroy()

        for bullet in self.bullets[:]:
            print(bullet)
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if self.ASTEROID_COUNT < 6:
            shuffle(self.Locations)

            for index, item in enumerate(self.Locations):
                self.asteroids.append(Asteroid(item, (150,150)))
                self.ASTEROID_COUNT += 1


    def _draw(self):

        self.screen.fill((0, 0, 0))

        StarryBackground = Background(f"Assets/Background/Stars/{self.BG_Frame}.png", [0, 0], (self.width, self.height))
        self.screen.blit(StarryBackground.image, StarryBackground.rect)

        RotaryStar1 = Background(f'Assets/Background/RotaryStar/{self.RS_Frame}.png', [210,500], (100,100))
        self.screen.blit(RotaryStar1.image, RotaryStar1.rect)

        RotaryStar2 = Background(f'Assets/Background/RotaryStar/{self.RS_Frame}.png', [1210,110], (100,100))
        self.screen.blit(RotaryStar2.image, RotaryStar2.rect)

        Blackhole = Background(f'Assets/Background/BH/{self.BH_Frame}.png', [815,350], (150,150))
        self.screen.blit(Blackhole.image, Blackhole.rect)

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        for player in self.__otherPlayers:
            game_objects.append(player)

        if len(self.npcs) > 0:
            for npc in self.npcs:
                game_objects.append(npc)

        return game_objects
    
    def __receiveMessage(self, ch, method, properties, body):
        """
        Receives messages from the server and handles them
        
        Parameters
        ----------
            ch : channel
            method :
            properties :
            body : json
        """
        #print(body)
        #converts bytes to dictionary
        bodyDic = ast.literal_eval(body.decode('utf-8'))
        #print(bodyDic)

        #if a player joins and they aren't yourself (broadcast also sends to self) and they aren't already in the game
        if bodyDic['Type'] == 'Join' and bodyDic['from'] != self.__messenger.user and bodyDic['from'] not in self.__playerIds:
            #print('\n' + str(bodyDic['Message']))
            
            self.__otherPlayers.append(Spaceship(bodyDic['Ship'][0], self.bullets.append))

            # append(Ship(bodyDic['Ship'][0], len(self.__otherPlayers)+1, bodyDic['Ship'][1]))
            self.__allPlayers.append(Spaceship(bodyDic['Ship'][0], self.bullets.append))
            

            self.__playerIds.append(bodyDic['from'])
            #print(bodyDic['from'])
         

        #if someone joins the game and requests what users are already in the game
        elif bodyDic['Type'] == 'Who' and bodyDic['from'] != self.__messenger.user:
            if len(self.__playerIds) == 0 and self.__host == False:
                self.__host = True
                #self.__asteroids = [Asteroid(self.__screen, 3), Asteroid(self.__screen, 3)]

            self.__sendMessage({'Type': 'Join',
                                'Message': self.__messenger.user + ' is in the game!',
                                'Ship': [self.spaceship.getLocation()]})
     
        elif bodyDic['Type'] == 'Event' and bodyDic['from'] != self.__messenger.user and bodyDic['from'] in self.__playerIds:
            print(bodyDic)
            for dics in bodyDic['Events']:
                #if player accelerates accelerate the given ship 
                if dics['Type'] == 'Accelerate':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].accelerate()
                if dics['Type'] == 'Rotate':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].rotate(clockwise=bool(dics['Clockwise']))
                if dics['Type'] == 'Shoot':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].shoot()
                if dics['Type'] == 'Stop':  
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].accelerate(0)
        
            
            
    def __sendMessage(self, bodyDic):
        """
        Sends a message to the server
        
        Parameters
        ----------
            bodyDic : dictionary
        """
        self.__messenger.send("broadcast", bodyDic)
