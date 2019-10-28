import pygame
from pygame.locals import *
import character
import dataLoad
import battleField
import random
import gun

class Enemy(pygame.sprite.Sprite):
    SHOT_PROB = 60
    SHOT_CAPACITY = 5
    def __init__(self, startpos, speed, types, imagePath, capacity=5):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = dataLoad.load_image(imagePath, -1)
        if types == 1:
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = startpos[0], startpos[1]
        self.types = types
        self.speed = speed
        self.SHOT_CAPACITY = capacity

    def update(self):
        if self.types == 1:
            if self.rect.midright[0] < 0:
                self.kill()
            self.rect.x += self.speed
        elif self.types == 2:
            if self.rect.midleft[0] > 1440:
                self.kill()
            self.rect.x -= self.speed
        self.gun()
        
    def gun(self):
        if not random.randrange(self.SHOT_PROB) and self.SHOT_CAPACITY != 0:
            gun.Bullet1(self.rect.topleft, self.speed, self.types, "Data/bullet1.bmp")
            self.SHOT_CAPACITY -= 1

class Enemy2(Enemy):
    def __init__(self, startpos, speed, types, imagePath, capacity=3):
        super().__init__(startpos, speed, types, imagePath, capacity=capacity)

    def gun(self):
        if not random.randrange(self.SHOT_PROB) and self.SHOT_CAPACITY != 0:
            gun.Bomb(self.rect.topleft, self.speed, self.types, "Data/bullet1.bmp")
            self.SHOT_CAPACITY -= 1