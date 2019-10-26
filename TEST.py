#!/usr/bin/env/python
# coding: utf-8
import pygame
from pygame.locals import *
import dataLoad
import sys
import os

SCR_RECT = Rect(0, 0, 640, 480)
TITLE, PLAY, GAMEOVER, CLEAR = (0, 1, 2, 3) #ゲームの状態

class Main:
    def __init__(self):
        pygame.init() #pygameモジュールの初期化
        screen = pygame.display.set_mode(SCR_RECT.size) #メイン画面の作成
        pygame.display.set_caption("TEST") #タイトルバーの文字列をセット

        self.load_images()
        self.load_sounds()

        self.init_game()
        clock = pygame.time.Clock() #clockオブジェクトの作成
        while True:
            clock.tick(60) #clockオブジェクトの更新
            self.clearorgameover()
            self.collision_detection()
            self.update()
            self.draw(screen)
            pygame.display.update() #画面の作成
            self.key_handler()

    def init_game(self):
        '''ゲームの初期化'''
        self.mycoin = 0
        self.game_state = TITLE #ゲーム状態をTITLEにする
        #スプライトグループの作成
        self.all = pygame.sprite.RenderUpdates()
        self.minecollige = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.item = pygame.sprite.Group()
        #デフォルトスプライトグループの登録
        Mine.containers = self.all, self.minecollige
        Block.containers = self.all, self.blocks
        Coin.containers = self.all, self.item
        #オブジェクトの作成
        self.map = Map("Data/MAP.map", self.all)
        self.mine = Mine((100, 900), self.blocks)
        self.count = ScoreCount()
        #カーソルの初期位置を指定
        self.cursor = 325

    def update(self):
        self.map.update()

    def draw(self, screen):
        if self.game_state == TITLE:
            #ゲーム状態がTITLEのとき、タイトル画面を描画
            Title(screen, self.cursor)

        elif self.game_state == PLAY:
            #ゲーム状態がPLAYのとき、スプライト、コイン枚数を描画
            self.map.draw()
            self.scroll(screen) #画面スクロール処理
            self.count.draw(screen)

        elif self.game_state == GAMEOVER:
            #ゲーム状態がGAMEOVERのとき、ゲームオーバー画面を描画
            Gameover(screen)

        elif self.game_state == CLEAR:
            #ゲーム状態がCLEARのとき、クリア画面を描画
            Clear(screen)

    def scroll(self, screen):
        '''画面のスクロール処理'''
        offsetx, offsety = self.calc_offset() 
        #画面の端ではスクロールしない
        if offsetx < 0:
            offsetx = 0
        elif offsetx > self.map.width - SCR_RECT.width:
            offsetx = self.map.width - SCR_RECT.width

        if offsety < 0:
            offsety = 0
        elif offsety > self.map.height - SCR_RECT.height:
            offsety = self.map.height - SCR_RECT.height

        #マップの一部を画面に描画
        screen.blit(self.map.surface, (0, 0), (offsetx, offsety, SCR_RECT.width, SCR_RECT.height))

    def calc_offset(self):
        '''オフセット(自機を中心としたときの画面の左上の座標)の計算'''
        offsetx = self.mine.rect.topleft[0] - SCR_RECT.width//2
        offsety = self.mine.rect.topleft[1] - SCR_RECT.height//2
        return offsetx, offsety
        
    def key_handler(self):
        '''キー入力受付'''
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #カーソル移動
            if self.game_state == TITLE:
                if event.type == KEYDOWN:
                    if event.key == K_UP and self.cursor != 325:
                        self.cursor -= 50
                    if event.key == K_DOWN and self.cursor != 375:
                        self.cursor += 50
                    if event.key == K_SPACE:
                        if self.cursor == 325:
                            #ゲーム開始
                            self.init_game()
                            self.game_state = PLAY
                        if self.cursor == 375:
                            pygame.quit()
                            sys.exit()
            #ゲーム終了後、スペースを押してゲーム状態をTITLEに
            if self.game_state == GAMEOVER or self.game_state == CLEAR:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.init_game()
                        self.game_state = TITLE

    def clearorgameover(self):
        '''条件を満たしていれば、ゲーム状態を変更する'''
        if self.mine.rect.y > 1000:
            self.game_state = GAMEOVER
            Gameover.coin = self.count.coin
        if self.count.coin == 30:
            self.game_state = CLEAR

    def collision_detection(self):
        '''アイテムの取得判定'''
        item_collided = pygame.sprite.groupcollide(self.minecollige, self.item, False, True)
        for item in item_collided.keys():
            self.coin_sound.play() #効果音を鳴らす
            self.count.addcoin() #コインの枚数を増やす

    def load_images(self):
        '''イメージのロード'''
        Mine.left_images = dataLoad.split_image("YELLOW_LEFT.bmp", "Data")
        Mine.right_images = dataLoad.split_image("YELLOW_RIGHT.bmp", "Data")
        Coin.images = dataLoad.split_image("coin.bmp", "data")
        Coin.image = Coin.images[0]
        Block.image = dataLoad.load_image("Block.bmp", "data")

    def load_sounds(self):
        '''効果音のロード'''
        #音ズレをなくすための処理
        pygame.mixer.quit()
        pygame.mixer.init(buffer=1024)
        self.coin_sound = dataLoad.load_sound("coin.wav", "data")

class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        #posの位置にブロックスプライトを配置
        self.rect.topleft = pos

class ScoreCount:
    '''アイテムの個数カウンター'''
    def __init__(self):
        self.coin = 0
        self.sysfont = pygame.font.SysFont(None, 40)

    def draw(self, screen):
        #コインの枚数を表示
        coin = "COIN : " + str(self.coin) 
        COIN = self.sysfont.render(coin, True, (0, 0, 0))
        screen.blit(COIN, (0, 0))

    def addcoin(self):
        self.coin += 1 #コインの枚数を一枚増やす

class Coin(pygame.sprite.Sprite):
    ANIMCYCLE = 16    #アニメーション速度
    frame = 0    #経過フレーム数

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        #posの位置にコインスプライトを配置
        self.rect.topleft = pos

    def update(self):
        #配置されているコインのアニメーションを更新
        self.frame +=1
        self.image = self.images[self.frame//self.ANIMCYCLE%2]

class Gameover:
    def __init__(self, screen):
        self.game_over_draw(screen)

    def game_over_draw(self, screen):
        '''ゲームオーバー画面を表示'''
        screen.fill((255, 255, 255)) #画面を白で塗りつぶす
        #フォントの作成
        gameoverfont = pygame.font.SysFont(None, 80)
        myfont = pygame.font.SysFont(None, 40)
        #文字の画像(Surface)の作成
        GAME_OVER = gameoverfont.render("GAME OVER", True, (0, 0, 0))
        PUSH_SPACE_KEY = myfont.render("PUSH SPACE KEY", True, (0, 0, 0))
        coin = "COIN : " + str(self.coin)
        COIN = myfont.render(coin, True, (0, 0, 0))
        #文字の描画
        screen.blit(GAME_OVER, (140, 110))
        screen.blit(PUSH_SPACE_KEY, (185, 300))
        screen.blit(COIN, (250, 170))

class Clear:
    def __init__(self, screen):
        self.game_clear_draw(screen)

    def game_clear_draw(self, screen):
        '''クリア画面の描画'''
        screen.fill((255, 255, 255)) #画面を白で塗りつぶす
        #フォントの作成
        gameclearfont = pygame.font.SysFont(None, 80)
        myfont = pygame.font.SysFont(None, 40)
        #文字の画像(Surface)の作成
        GAME_CLEAR = gameclearfont.render("GAME CLEAR", True, (0, 0, 0))
        PUSH_SPACE_KEY = myfont.render("PUSH SPACE KEY", True, (0, 0, 0))
        #文字の描画
        screen.blit(GAME_CLEAR, (140, 110))
        screen.blit(PUSH_SPACE_KEY, (185, 300))

class Title:
    def __init__(self, screen, cursor):
        self.game_title_draw(screen, cursor)

    def game_title_draw(self, screen, cursor):
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

class Character:
    '''キャラクタークラス
    自機クラスや敵クラスを作る際に継承して使う
    動くキャラに共通するデータやメソッドをまとめたクラス'''
    MOVE_SPEED = 0.0    #移動速度
    JUMP_SPEED = 0.0    #ジャンプの速度

    ANIMCYCLE = 8    #アニメーション速度
    GRAVITY = 0.2    #重力の大きさ

    frame = 0    #経過フレーム数
    on_FLOOR = False    #床についているかどうか

    def __init__(self):
        #継承先のクラスでオーバーライドするので必要ない
        pass

    def fall(self):
        #キャラが床についていないとき、重力をかける
        if not self.on_FLOOR:
            self.fpvy += self.GRAVITY

    def collision_x(self):
        '''X方向のブロックとの衝突判定'''
        width = self.rect.width
        height = self.rect.height

        #X方向の移動先の座標と矩形を求める
        newx = self.fpx + self.fpvx
        newrect = Rect(newx, self.fpy, width, height)
        
        #ブロックとの衝突判定
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide: #衝突するブロックあり
                if self.fpvx > 0: #右に移動中に衝突
                    #めり込まないように調整して速度を0に
                    self.fpx = block.rect.left - width
                    self.fpvx = 0
                elif self.fpvx < 0: #左に移動中に衝突
                    self.fpx = block.rect.right
                    self.fpvx = 0
                break
            else:
                #衝突ブロックがない場合、位置を更新
                self.fpx = newx

    def collision_y(self):
        '''Y方向のブロックとの衝突判定'''
        width = self.rect.width
        height = self.rect.height

        #Y方向の移動先の座標と矩形を求める
        newy = self.fpy + self.fpvy
        newrect = Rect(self.fpx, newy, width, height)

        #ブロックとの衝突判定
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:
                if self.fpvy > 0:
                    self.fpy = block.rect.top - height
                    self.fpvy = 0
                    #落下中に衝突したときには、床の上にいる
                    self.on_FLOOR = True
                elif self.fpvy < 0:
                    self.fpy = block.rect.bottom
                    self.fpvy = 0
                break
            else:
                #衝突ブロックがない場合、位置を更新
                self.fpy = newy
                #衝突していないときには、床の上にいない
                self.on_FLOOR = False

class Mine(pygame.sprite.Sprite, Character):
    '''自機クラス'''
    def __init__(self, startpos, blocks):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.MOVE_SPEED = 3.0 #移動速度を設定
        self.JUMP_SPEED = 8.0 #ジャンプ速度を設定


        self.right_image = self.right_images[0] #右向きのイメージを設定
        self.left_image = self.left_images[0] #左向きのイメージを設定
        self.image = self.right_image 
        self.blocks = blocks #衝突判定用のブロックスプライトグループを設定
        self.rect = self.image.get_rect() 
        self.rect.x, self.rect.y = startpos[0], startpos[1] #座標の設定
        #浮動小数点の位置
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        #浮動小数点の速度
        self.fpvx = 0.0
        self.fpvy = 0.0

        #床についているか
        self.on_FLOOR = False

    def update(self):
        '''スプライトの更新'''
        #キー入力取得
        pressed_keys = pygame.key.get_pressed()

        #左右移動
        if pressed_keys[K_RIGHT]:
            self.image = self.right_image #画像を右向きに変える
            self.frame += 1 
            self.image = self.right_images[self.frame//self.ANIMCYCLE%2] #アニメーションの更新
            self.fpvx = self.MOVE_SPEED 
        elif pressed_keys[K_LEFT]:
            self.image = self.left_image #画像を左向きに変える
            self.frame += 1
            self.image = self.left_images[self.frame//self.ANIMCYCLE%2] 
            self.fpvx = -self.MOVE_SPEED
        else:
            self.fpvx = 0.0
        #スペースが押されたとき
        if pressed_keys[K_SPACE]:
            if self.on_FLOOR:
                self.fpvy = -self.JUMP_SPEED #上向きに初速度を与える
                self.on_FLOOR = False
        #シフトが押されたとき
        if pressed_keys[K_LSHIFT]:
            #移動速度を半分にし、アニメーション速度を二倍にする
            self.MOVE_SPEED = 1.5
            self.ANIMCYCLE = 16
        else:
            self.MOVE_SPEED = 3.0
            self.ANIMCYCLE = 8

        #落下処理
        self.fall()
        
        #X方向、Y方向の衝突判定処理
        self.collision_x()
        self.collision_y()
  
        #self.rectの更新
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

class Map:
    GS = 32    #グリッドサイズ
    def __init__(self, filename, all):
        self.load(filename) #ファイルからマップをロード
        self.all = all
        #ファイルからロードしたマップの大きさのsurfaceを作成
        self.surface = pygame.Surface((self.col*self.GS, self.row*self.GS)).convert()

    def draw(self):
        '''マップ内スプライトの描画'''
        self.surface.fill((255, 255, 255))
        self.all.draw(self.surface)

    def update(self):
        '''マップ内スプライトの更新'''
        self.all.update()

    def load(self, filename):
        '''マップをロードしてスプライトを作成'''
        map = []
        fp = open(filename, "r")
        for line in fp:
            line = line.rstrip()
            map.append(list(line)) 
            self.row = len(map)
            self.col = len(map[0])
        self.width = self.col * self.GS
        self.height = self.row * self.GS
        fp.close()

        '''マップからスプライトを配置
        1のときブロックを配置、2のときコインを配置'''
        for i in range(self.row):
            for j in range(self.col):
                if map[i][j] == '1':
                    Block((j*self.GS, i*self.GS))
                if map[i][j] == '2':
                    Coin((j*self.GS, i*self.GS))

if __name__ == "__main__":
    Main()

