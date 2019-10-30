import pygame
from pygame.locals import *
import enemy
import random

def generation():
    if random.randint(0,80) == 0:
        posX = random.randint(0,1)*1440
        posY = random.randint(0,250)+400
        speed = random.randint(2,4)
        types = 1 if posX == 0 else 2

        #出現する敵の種類
        kind = random.randint(0,150)
        if kind >= 0 and kind < 110:
            enemy.Enemy((posX, posY), speed, types, imagePath="Data/Enemy1.bmp")
        elif kind >= 110 and kind < 130:
            enemy.Enemy2((posX, posY), speed, types, imagePath="Data/Enemy2.bmp")
        elif kind >= 130 and kind < 150:
            enemy.Enemy3((posX, posY-100), speed, types, imagePath="Data/Enemy3.bmp")