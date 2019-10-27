import pygame
from pygame.locals import *

def gameover_draw(screen):
    '''ゲームオーバー画面を表示'''
    screen.fill((255, 255, 255)) #画面を白で塗りつぶす
    print("A")
    #フォントの作成
    gameoverfont = pygame.font.SysFont(None, 180)
    myfont = pygame.font.SysFont(None, 140)
    #文字の画像(Surface)の作成
    GAME_OVER = gameoverfont.render("GAME OVER", True, (0, 0, 0))
    PUSH_SPACE_KEY = myfont.render("PUSH SPACE KEY", True, (0, 0, 0))
    #文字の描画
    screen.blit(GAME_OVER, (600, 400))
    screen.blit(PUSH_SPACE_KEY, (185, 300))

    
def gametitle_draw(screen, cursor):
    '''タイトル画面の描画'''
    screen.fill((255, 255, 255)) #画面を白で塗りつぶす
    #フォントの作成
    gametitlefont = pygame.font.SysFont(None, 120)
    gamestartmenufont = pygame.font.SysFont(None, 60)
    #文字の画像(Surface)の作成
    GAME_TITLE = gametitlefont.render("GAME", True, (0, 0, 0))
    GAME_START = gamestartmenufont.render("START", True, (0, 0, 0))
    GAME_EXIT = gamestartmenufont.render("QUIT", True, (0, 0, 0))
    GAME_CURSOR = gamestartmenufont.render(">", True, (255, 0, 0))
    #文字の描画
    screen.blit(GAME_TITLE, (180, 70))
    screen.blit(GAME_START, (240, 330))
    screen.blit(GAME_EXIT, (255, 380))
    screen.blit(GAME_CURSOR, (190, cursor))