import pygame
from pygame.locals import *
import dataLoad
import map
import gameStatus
import mine
import enemy
import gun
import battleField
import sys

SCR_RECT = Rect(0, 0, 1440, 810)
TITLE, PLAY, GAMEOVER = (0, 1, 2)

class Main:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("GAME")

        self.init_mixer()
        self.init_game()
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update(screen)
            self.infoUpdate()
            self.key_handler()
            pygame.display.update()
            
    def init_game(self):
        '''ゲームの初期化'''
        self.game_state = TITLE
        self.all = pygame.sprite.RenderUpdates()
        self.mineCollige = pygame.sprite.Group()
        self.enemyCollige = pygame.sprite.Group()
        self.mineBulletsCollige = pygame.sprite.Group()
        self.enemyBulletsCollige = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        mine.Mine.containers = self.all, self.mineCollige
        map.Block.containers = self.all, self.blocks
        enemy.Enemy.containers = self.all, self.enemyCollige
        gun.Bullet1.containers = self.all, self.enemyBulletsCollige
        gun.MyBullet.containers = self.all, self.mineBulletsCollige

        self.map = map.Map("Data/MAP.map", self.all, SCR_RECT, GS=32)
        self.mine = mine.Mine((200, 600), self.blocks, "Data/YELLOW.bmp")

    def update(self, screen):
        if self.game_state == TITLE:
            gameStatus.gametitle_draw(screen)

        elif self.game_state == PLAY:
            battleField.generation()
            self.collideBullets()
            self.map.update(screen, self.mine)
            self.map.draw()

        elif self.game_state == GAMEOVER:
            gameStatus.gameover_draw(screen)
        
    def key_handler(self):
        '''キー入力受付'''
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if self.game_state == TITLE:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.init_game()
                        self.game_state = PLAY
            if self.game_state == GAMEOVER:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.init_game()
                        self.game_state = TITLE

    def infoUpdate(self):
        '''条件を満たしていれば、ゲーム状態を変更する'''
        if self.liveOrDie():
            self.game_state = GAMEOVER
        if self.shootDown():
            print("Good!")

    def shootDown(self):
        collide = pygame.sprite.groupcollide(self.mineBulletsCollige, self.enemyCollige, True, True)
        for enemy in collide.keys():
            return 1
        return 0

    def liveOrDie(self):
        collide = pygame.sprite.groupcollide(self.mineCollige, self.enemyBulletsCollige, False, False)
        for enemy in collide.keys():
            return 1
        collide = pygame.sprite.groupcollide(self.mineCollige, self.enemyCollige, False, False)
        for enemy in collide.keys():
            return 1
        if self.mine.rect.y > 1000:
            return 1
        return 0

    def collideBullets(self):
        collide = pygame.sprite.groupcollide(self.blocks, self.enemyBulletsCollige, False, True)
        for enemy in collide.keys():
            pass

    def init_mixer(self):
        pygame.mixer.quit()
        pygame.mixer.init(buffer=1024)

if __name__ == "__main__":
    Main()