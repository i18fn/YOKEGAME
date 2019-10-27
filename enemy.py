import pygame
from pygame.locals import *
import character
import dataLoad
import battleField
import random
import gun

class Enemy(pygame.sprite.Sprite):
    SHOT_PROB = 40
    SHOT_CAPACITY = 5
    def __init__(self, startpos, speed, types, imagePath, capacity=5):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = dataLoad.split_images(imagePath)[0]
        self.right_image = self.image
        self.left_image = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = startpos[0], startpos[1]
        self.type = types
        self.speed = speed
        self.SHOT_CAPACITY = capacity

    def update(self):
        if self.type == 1:
            if self.rect.midright[0] < 0:
                self.kill()
            self.rect.x += self.speed
        elif self.type == 2:
            if self.rect.midleft[0] > 1440:
                self.kill()
            self.rect.x -= self.speed
        if not random.randrange(self.SHOT_PROB) and self.SHOT_CAPACITY != 0:
            gun.Gun1((self.rect.left, self.rect.centery), self.speed)
            self.SHOT_CAPACITY -= 1