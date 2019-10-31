import pygame
from pygame.locals import *
    
def gametitle_draw(screen, cursor_pos):
    screen.fill((255, 255, 255))

    gametitlefont = pygame.font.SysFont(None, 180)
    gamestartmenufont = pygame.font.SysFont(None, 100)

    if cursor_pos == 520:
        GAME_START_COLOR = (255, 0, 0)
    else:
        GAME_START_COLOR = (0, 0, 0)
    if cursor_pos == 610:
        GAME_EXIT_COLOR = (255, 0, 0)
    else:
        GAME_EXIT_COLOR = (0, 0, 0)

    GAME_TITLE = gametitlefont.render("YOKERO", True, (0, 0, 0))
    GAME_START = gamestartmenufont.render("START", True, GAME_START_COLOR)
    GAME_EXIT = gamestartmenufont.render("QUIT", True, GAME_EXIT_COLOR)
    CURSOR = gamestartmenufont.render(">", True, (0, 0, 0))

    screen.blit(GAME_TITLE, (400, 150))
    screen.blit(GAME_START, (550, 530))
    screen.blit(GAME_EXIT, (575, 620))
    screen.blit(CURSOR, (500, cursor_pos))

def gameover_draw(screen, score):
    gameoverfont = pygame.font.SysFont(None, 180)
    scorefont = pygame.font.SysFont(None, 140)
    GAME_OVER = gameoverfont.render("GAME OVER", True, (0, 0, 0))
    SCORE = scorefont.render(("YOUR SCORE : " + str(score)), True, (0, 0, 0))
    screen.blit(GAME_OVER, (300, 300))
    screen.blit(SCORE, (200, 450))