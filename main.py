import pygame
from pygame.locals import *
import dataLoad
import map
import gameStatus
import mine
import enemy
import gun
import sys
import os

SCR_RECT = Rect(0, 0, 1088, 612)
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
            self.draw(screen)
            self.map.update(screen, self.mine)
            self.key_handler()
            pygame.display.update() #画面の作成
            

    def init_game(self):
        '''ゲームの初期化'''
        self.game_state = PLAY #ゲーム状態をTITLEにする
        #スプライトグループの作成
        self.all = pygame.sprite.RenderUpdates()
        self.collige = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        #デフォルトスプライトグループの登録
        mine.Mine.containers = self.all, self.collige
        map.Block.containers = self.all, self.blocks

        #オブジェクトの作成
        self.map = map.Map("Data/MAP.map", self.all, SCR_RECT, GS=32)
        self.mine = mine.Mine((100, 100), self.blocks, "Data/YELLOW_RIGHT.bmp")
        #カーソルの初期位置を指定


    def draw(self, screen):
        if self.game_state == TITLE:
            pass

        elif self.game_state == PLAY:
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
                    pass

    def clearorgameover(self):
        '''条件を満たしていれば、ゲーム状態を変更する'''
        if self.mine.rect.y > 1000:
            self.game_state = GAMEOVER

    def init_mixer(self):
        '''効果音のロード'''
        #音ズレをなくすための処理
        pygame.mixer.quit()
        pygame.mixer.init(buffer=1024)

if __name__ == "__main__":
    Main()