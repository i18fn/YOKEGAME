import pygame
from pygame.locals import *
import dataLoad

class Bullet1(pygame.sprite.Sprite):
    def __init__(self, pos, speed, types, imagePath):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = dataLoad.load_image(imagePath, -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        if types == 1:
            self.speed = speed + 2
        elif types == 2:
            self.speed = -1 * (speed + 2)
        self.types = types

    def update(self):
        if self.types == 1:
            if self.rect.midright[0] < 0:
                self.kill()
        elif self.types == 2:
            if self.rect.midleft[0] > 1440:
                self.kill()
        self.rect.x += self.speed
    
class MyBullet(Bullet1):
    def __init__(self, pos, speed, types, imagePath):
        super().__init__(pos, speed, types, imagePath)
        if types == 1:
            self.speed += 3
        elif types == 2:
            self.speed -= 3
    def update(self):
        super().update()