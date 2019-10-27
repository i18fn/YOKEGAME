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
import os

SCR_RECT = Rect(0, 0, 1440, 810)
TITLE, PLAY, GAMEOVER, CLEAR = (0, 1, 2, 3)

class Main:
    def __init__(self):
        pygame.init() #pygameモジュールの初期化
        screen = pygame.display.set_mode(SCR_RECT.size) #メイン画面の作成
        pygame.display.set_caption("GAME") #タイトルバーの文字列をセット

        self.init_game()
        self.init_mixer()
        clock = pygame.time.Clock() #clockオブジェクトの作成
        while True:
            clock.tick(60) #clockオブジェクトの更新
            self.update(screen)
            self.infoUpdate()
            self.key_handler()
            pygame.display.update() #画面の作成
            

    def init_game(self):
        '''ゲームの初期化'''
        self.game_state = PLAY #ゲーム状態をTITLEにする
        #スプライトグループの作成
        self.all = pygame.sprite.RenderUpdates()
        self.mineCollige = pygame.sprite.Group()
        self.enemyCollige = pygame.sprite.Group()
        self.mineBulletsCollige = pygame.sprite.Group()
        self.enemyBulletsCollige = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        #デフォルトスプライトグループの登録
        mine.Mine.containers = self.all, self.mineCollige
        map.Block.containers = self.all, self.blocks
        enemy.Enemy.containers = self.all, self.enemyCollige
        gun.Bullet1.containers = self.all, self.enemyBulletsCollige
        gun.MyBullet.containers = self.all, self.mineBulletsCollige

        #オブジェクトの作成
        self.map = map.Map("Data/MAP.map", self.all, SCR_RECT, GS=32)
        self.mine = mine.Mine((200, 600), self.blocks, "Data/YELLOW.bmp")
        
        #カーソルの初期位置を指定


    def update(self, screen):
        if self.game_state == TITLE:
            pass

        elif self.game_state == PLAY:
            battleField.generation()
            self.map.update(screen, self.mine)
            self.map.draw()

        elif self.game_state == GAMEOVER:
            gameStatus.gameover_draw(screen)

        elif self.game_state == CLEAR:
            pass
        
    def key_handler(self):
        '''キー入力受付'''
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #カーソル移動
            if self.game_state == TITLE:
                if event.type == KEYDOWN:
                    pass
            #ゲーム終了後、スペースを押してゲーム状態をTITLEに
            if self.game_state == GAMEOVER or self.game_state == CLEAR:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.init_game()
                        self.game_state = PLAY

    def infoUpdate(self):
        '''条件を満たしていれば、ゲーム状態を変更する'''
        if self.mine.rect.y > 1000 or self.liveOrDie():
            self.game_state = GAMEOVER
        if self.shootDown():
            print("Good!")

    def shootDown(self):
        collide = pygame.sprite.groupcollide(self.mineBulletsCollige, self.enemyCollige, False, True)
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
        return 0

    def init_mixer(self):
        '''効果音のロード'''
        #音ズレをなくすための処理
        pygame.mixer.quit()
        pygame.mixer.init(buffer=1024)

if __name__ == "__main__":
    Main()