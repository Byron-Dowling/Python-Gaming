import pygame
import ast
import random
from copy import deepcopy


class GameDriver:
    """
    The main driver that handles all game functionality.
    
    Attributes
    ----------
    __host : 
    __screen : pygame.Display
        The screen the game is played on
    __clock : pygame.time.Clock
        The clock that controls the fps
    __fps : int
        The frames per second
    __delta : int
        The time between frames
    __running : bool
        Whether or not the game is running
    __asteroidCrash : pygame.mixer.Sound
        The sound that plays when a bullet hits an asteroid 
    __backgroundColor : tuple
        The background color of the game in (R,G,B) format
    __ship : Ship()
        The player's ship
    __asteroids : list
        The list of asteroids
    __healthBar : HealthBar()
        The health bar of the player
    __scores : Scores()
        The scores of the game
    __background : Background()
        The background of the game
    multiplayer :
        Whether or not the game is multiplayer
    __playerIds : list
        list of playId's in the game
    __otherPlayer : list
        list of other players in the game
    __allPlayers : list 
        list of all player's ships in the game

    Methods
    -------
    GameLoop()
        The main game loop
    __Draw()
        Draws all game objects
    __handleEvents()
        Handles all pygame events in the game
    __CheckCollision()
        Checks for bullet and asteroid collisions
    __newAsteroids()
        Creates new asteroids 
    __receiveMessage(message)
        Receives a message from the server
    __sendMessage(message)
        Sends a message to the server
    
    """
    def __init__(self, title, backgroundColor = (255,255,255), height = 1200, width = 770, fps = 30, multiplayer = None):
        """
        Parameters
        ----------
            title : 
            backgroundColor : tuple, optional
                Defaults to (255,255,255)
            height : int, optional
                Defaults to 1200
            width : int, optional
                Defaults to 770
            fps : int, optional
                Defaults to 30
            multiplayer : optional 
                Defaults to None
        """
        self.__host = False

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('Sounds/ambient-dream.mp3')
        pygame.mixer.music.set_volume(.05)
        pygame.mixer.music.play(-1)
        self.__backgroundColor = backgroundColor
        
        self.__screen = pygame.display.set_mode((height,width))
        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0
        self.__running = True
        self.__asteroidCrash = pygame.mixer.Sound('Sounds/explosion.wav')

        pygame.display.set_caption(title)

        #always 0 bc player one, spawns at random location inside buffer
        self.__ship = Ship((random.randrange(100, self.__screen.get_width() - 100), random.randrange(100, self.__screen.get_height() - 100)), 0)
        self.__asteroids = []
        self.__healthBar = HealthBar(self.__screen)

        #sends a message that someone new has joined the game
        self.__messenger = multiplayer

        self.__scores = Scores(self.__messenger.user, self.__ship.getColor())
        
        if multiplayer != None:
            self.__messenger.setCallback(self.__receiveMessage)
        
            #sends a message asking for what players are already in the game
            self.__sendMessage(
                {'Type': 'Who'})

            self.__sendMessage(
                {'Type': 'Join',
                'Message': self.__messenger.user + ' has joined the game!',
                'Ship': [self.__ship.getLocation(), self.__ship.getVelocity()]})
            
            self.__playerIds = []

        self.__otherPlayers = []
        self.__allPlayers = [self.__ship]

        self.__background = Background(
            [
            'Environment/Backgrounds/Condensed/Starry background  - Layer 01 - Void.png',
            'Environment/Backgrounds/Condensed/Starry background  - Layer 02 - Stars.png',
            'Environment/Backgrounds/Condensed/Starry background  - Layer 03 - Stars.png'
            ], 9,self.__screen, 4
        )