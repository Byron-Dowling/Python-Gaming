#from game_multiplayer import SpaceRocks
from game_npc_ex import SpaceRocks
from multi import SpaceRocks
from messenger import Messenger
import sys

"""
 
 ████████╗ ██████╗     ██████╗  ██████╗     ██╗     ██╗███████╗████████╗
 ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔═══██╗    ██║     ██║██╔════╝╚══██╔══╝
    ██║   ██║   ██║    ██║  ██║██║   ██║    ██║     ██║███████╗   ██║   
    ██║   ██║   ██║    ██║  ██║██║   ██║    ██║     ██║╚════██║   ██║   
    ██║   ╚██████╔╝    ██████╔╝╚██████╔╝    ███████╗██║███████║   ██║   
    ╚═╝    ╚═════╝     ╚═════╝  ╚═════╝     ╚══════╝╚═╝╚══════╝   ╚═╝   
                                                                        
 
    
    - Find a different projectile or fix the rotation
        - Rotation is happening the wrong way
    - Do Collision detection between projectiles and players
"""


"""
    Example Run commands:
        python ex_05.py game1 player-1 'player-12023!!!!!'

        python .\__main__.py  game-01 player-01 'player-022023!!!!!'
        python .\__main__.py  game-01 player-02 'player-022023!!!!!'
"""
if len(sys.argv) < 3:
    print("Need: exchange and player ")
    print("Example: python ex05.py game-01 player-02")
    sys.exit()

game = sys.argv[1]
player = sys.argv[2]
creds = {
    "exchange": game,
    "port": "5672",
    "host": "terrywgriffin.com",
    "user": player,
    "password": player + "2023!!!!!",
}

if __name__ == "__main__":


    
    multiplayer = Messenger(creds)

#GC = GameController(multiplayer = multiplayer)
    #space_rocks = SpaceRocks()
    space = SpaceRocks(multiplayer)
    space.main_loop()
    #space_rocks.main_loop()
