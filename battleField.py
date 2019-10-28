import pygame
from pygame.locals import *
import enemy
import random

def generation():
    if random.randint(0,80) == 0:
        posX = random.randint(0,1)*1440
        posY = random.randint(0,150)+500
        speed = random.randint(2,4)
        types = 1 if posX == 0 else 2
        enemy.Enemy2((posX, posY), speed, types, imagePath="Data/Enemy1.bmp")