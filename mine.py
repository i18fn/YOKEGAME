import pygame
from pygame.locals import *
import dataLoad
import character

class Mine(pygame.sprite.Sprite):
    '''自機クラス'''
    MOVE_SPEED = 0.0    #移動速度
    JUMP_SPEED = 0.0    #ジャンプの速度
    ANIMCYCLE = 8    #アニメーション速度
    GRAVITY = 0.2    #重力の大きさ
    frame = 0    #経過フレーム数
    on_FLOOR = False    #床についているかどうか
    def __init__(self, startpos, blocks, imagePath):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.MOVE_SPEED = 3.0 #移動速度を設定
        self.JUMP_SPEED = 8.0 #ジャンプ速度を設定

        self.images = dataLoad.split_images(imagePath) #右向き基準
        self.right_images = self.images
        self.right_image  = self.right_images[0]
        self.left_images  = dataLoad.split_images(imagePath, flip=1)
        self.left_image   = self.left_images[0]
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