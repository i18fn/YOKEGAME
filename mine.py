import pygame
from pygame.locals import *
import dataLoad
import gun

class Mine(pygame.sprite.Sprite):
    '''自機クラス'''
    MOVE_SPEED = 6    #移動速度
    JUMP_SPEED = 10.0    #ジャンプの速度
    ANIMCYCLE = 8    #アニメーション速度
    GRAVITY = 0.4    #重力の大きさ
    MAX_JUMP_COUNT = 3    #ジャンプ段数の回数
    frame = 0    #経過フレーム数
    on_FLOOR = False    #床についているかどうか
    waittime = 11   #最初の待ち時間用
    guns_wait = 8   #弾丸発射の待ち時間
    types = 1   #向いている方向(1:右向き, 2:左向き)
    def __init__(self, startpos, blocks, imagePath):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = dataLoad.split_images(imagePath, size=26) #右向き基準
        self.right_images = self.images
        self.right_image  = self.right_images[0]
        self.left_images  = dataLoad.split_images(imagePath, size=26, flip=1)
        self.left_image   = self.left_images[0]
        self.image = self.right_image
        self.blocks = blocks
        self.rect = self.image.get_rect() 
        self.rect.x, self.rect.y = startpos[0], startpos[1]

        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = 0.0
        self.fpvy = 0.0
        
        self.on_FLOOR = False
        self.t2 = 0    #連射の間隔を測るための変数
        self.jump_count = 0

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_RIGHT]:
            self.types = 1
            self.image = self.right_image #画像を右向きに変える
            self.frame += 1 
            self.image = self.right_images[self.frame//self.ANIMCYCLE%2] #アニメーションの更新
            self.fpvx = self.MOVE_SPEED 
        elif pressed_keys[K_LEFT]:
            self.types = 2
            self.image = self.left_image #画像を左向きに変える
            self.frame += 1
            self.image = self.left_images[self.frame//self.ANIMCYCLE%2] 
            self.fpvx = -self.MOVE_SPEED
        else:
            self.fpvx = 0.0

        if pressed_keys[K_UP]:
            if self.on_FLOOR:
                self.fpvy = -self.JUMP_SPEED #上向きに初速度を与える
                self.on_FLOOR = False
                self.jump_count = 1
            elif not self.prev_button and self.jump_count < self.MAX_JUMP_COUNT:
                self.fpvy = -self.JUMP_SPEED
                self.jump_count += 1
        
        if pressed_keys[K_SPACE] and self.waittime > self.guns_wait:
            gun.MyBullet(self.rect.topleft, self.MOVE_SPEED, self.types, "Data/bullet1.bmp")
            self.waittime = 0
        else:
            self.waittime += 1

        #シフトが押されたとき
        if pressed_keys[K_LSHIFT]:
            #移動速度を半分にし、アニメーション速度を二倍にする
            self.MOVE_SPEED = 1.5
            self.ANIMCYCLE = 16
        else:
            self.MOVE_SPEED = 3.0
            self.ANIMCYCLE = 8

        if not self.on_FLOOR:
            self.fpvy += self.GRAVITY 

        self.collision_x()
        self.collision_y()
  
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

        self.prev_button = pressed_keys[K_UP]    #直前のスペースキーの状態

    def collision_x(self):
        width = self.rect.width
        height = self.rect.height

        newx = self.fpx + self.fpvx
        newrect = Rect(newx, self.fpy, width, height)
        
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:
                if self.fpvx > 0:
                    self.fpx = block.rect.left - width
                    self.fpvx = 0
                elif self.fpvx < 0:
                    self.fpx = block.rect.right
                    self.fpvx = 0
                break
            else:
                self.fpx = newx

    def collision_y(self):
        '''Y方向のブロックとの衝突判定'''
        width = self.rect.width
        height = self.rect.height

        newy = self.fpy + self.fpvy
        newrect = Rect(self.fpx, newy, width, height)

        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:
                if self.fpvy > 0:
                    self.fpy = block.rect.top - height
                    self.fpvy = 0
                    self.on_FLOOR = True
                    self.jump_count = 0
                elif self.fpvy < 0:
                    self.fpy = block.rect.bottom
                    self.fpvy = 0
                break
            else:
                self.fpy = newy
                self.on_FLOOR = False