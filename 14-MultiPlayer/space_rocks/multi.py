import pygame

from models import Asteroid, Spaceship, NPC
from utils import get_random_position, load_sprite, print_text
import ast
import messenger

import pygame
import math
import random
from pygame.math import Vector2
import sys


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self, multiplayer=None):
        self._init_pygame()
        # current_w = 1680, current_h = 1050
        # self.screen = pygame.display.set_mode((1024, 768))
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.background = load_sprite("space", False)

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

        #print(self.__allPlayers)


        self.npcs = []

        self.started = False

        self.npcs.append(
            NPC(
                (self.width * 0.05, self.height * 0.05),
                self.bullets.append,
                "space_ship5_40x40",
                [self.spaceship],
                other_npcs=self.npcs,
            )
        )

        self.npcs.append(
            NPC(
                (self.width * 0.95, self.height * 0.95),
                self.bullets.append,
                "space_ship6_40x40",
                [self.spaceship],
                other_npcs=self.npcs,
            )
        )

        # Griffin changed this to 1 so it would only generate 1 asteroid :)
        for _ in range(0):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def other_npcs(self):
        return self.npcs

    def main_loop(self):
        while True:
            self._handle_input()
            if self.started:
                self._process_game_logic()
            # print(self.spaceship.getAttributes())
            self._draw()
            

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

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    break

        if len(self.npcs) > 0:
            for npc in self.npcs:
                npc.choose_target()
                npc.rotate()
                npc.follow_target()
                # npc.check_shoot()

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            print(bullet)
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # if not self.asteroids and self.spaceship:
        #     self.message = "You won!"

    def _draw(self):
        # self.screen.blit(self.background, (0, 0))

        self.screen.fill((0, 0, 0))
        # print(self.multiplayer)

        for game_object in self._get_game_objects():
            # print(game_object)
            game_object.draw(self.screen)

        # for player in self.__otherPlayers:
        #     player.draw(self.screen)
        
        #self.spaceship.draw(self.screen)

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

        # if self.__otherPlayers:
        #     game_objects.append(self.__otherPlayers)

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
