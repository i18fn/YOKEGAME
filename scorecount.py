import pygame
from pygame.locals import *

class ScoreCount:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont(None, 80)

    def addScore(self, score):
        self.score += score

    def getScore(self):
        return self.score
    
    def draw(self, screen):
        score = "SCORE : " + str(self.score) 
        score = self.font.render(score, True, (0, 0, 0))
        screen.blit(score, (0, 0))