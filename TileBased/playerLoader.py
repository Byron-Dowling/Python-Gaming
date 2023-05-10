"""
    Author:   Byron Dowling, Deangelo Brown, Izzy Olaemimimo
    Class:    5443 2D Python Gaming
"""

import os
import pprint
from random import shuffle

"""
    Object definition to hold sprite information

    Is necessary primarily because the sprite functions have a differing
    number of frames such as Idle being 6 frames but attack being 8 etc.
"""
characterSprite = {
    "Name": "",
    "Screen Name": "",
    "Action": {
        "Die": {
            "imagePath": "",
            "frameCount": 0
        },

        "Idle": {
            "imagePath": "",
            "frameCount": 0
        },

        "Move": {
            "imagePath": "",
            "frameCount": 0
        },

         "Roll": {
            "imagePath": "",
            "frameCount": 0
        },
         "Shoot": {
            "imagePath": "",
            "frameCount": 0
        },
         "Whip_Attack": {
            "imagePath": "",
            "frameCount": 0
        },
        "Whip_Swing": {
            "imagePath": "",
            "frameCount": 0
        }
    }
}


## To be used for pseudo-random character selection
class PlayerSelector:

    def __init__ (self):
        self.loadCharacter()
        self.player = self.getPlayer()

    def loadCharacter(self):
        characterSprite["Action"]["Shoot"]["imagePath"] = fr'Sprites/Shoot'
        characterSprite["Action"]["Shoot"]["frameCount"] = len(os.listdir(characterSprite["Action"]["Shoot"]["imagePath"]))
        characterSprite["Action"]["Die"]["imagePath"] = fr'Sprites/Die'
        characterSprite["Action"]["Die"]["frameCount"] = len(os.listdir(characterSprite["Action"]["Die"]["imagePath"]))
        characterSprite["Action"]["Idle"]["imagePath"] = fr'Sprites/Idle'
        characterSprite["Action"]["Idle"]["frameCount"] = len(os.listdir(characterSprite["Action"]["Idle"]["imagePath"]))
        characterSprite["Action"]["Move"]["imagePath"] = fr'Sprites/Move'
        characterSprite["Action"]["Move"]["frameCount"] = len(os.listdir(characterSprite["Action"]["Move"]["imagePath"]))
        characterSprite["Action"]["Roll"]["imagePath"] = fr'Sprites/Roll'
        characterSprite["Action"]["Roll"]["frameCount"] = len(os.listdir(characterSprite["Action"]["Roll"]["imagePath"]))
        characterSprite["Action"]["Whip_Attack"]["imagePath"] = fr'Sprites/Whip_Attack'
        characterSprite["Action"]["Whip_Attack"]["frameCount"] = len(os.listdir(characterSprite["Action"]["Whip_Attack"]["imagePath"]))
        characterSprite["Action"]["Whip_Swing"]["imagePath"] = fr'Sprites/Whip_Swing'
        characterSprite["Action"]["Whip_Swing"]["frameCount"] = len(os.listdir(characterSprite["Action"]["Whip_Swing"]["imagePath"]))

    def sanityCheck(self):
        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(self.player)

    def getPlayer(self):
        return characterSprite

if __name__ == '__main__':
    Indy = PlayerSelector()
    Indy.sanityCheck()
    print("It's not about the age, it's about the mileage")

