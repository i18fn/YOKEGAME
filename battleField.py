import pygame
from pygame.locals import *
import enemy
import random

def generation():
    if random.randint(0,10) == 0:
        posX = random.randint(0,1)*1440
        posY = random.randint(0,200)+400
        speed = random.randint(2,6)
        types = 1 if posX == 0 else 2
        enemy.Enemy((posX, posY), speed, types, imagePath="Data/coin.bmp")