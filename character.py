import pygame
from pygame.locals import *

class Character:
    MOVE_SPEED = 0.0    #移動速度
    JUMP_SPEED = 0.0    #ジャンプの速度

    ANIMCYCLE = 8    #アニメーション速度
    GRAVITY = 0.2    #重力の大きさ

    frame = 0    #経過フレーム数
    on_FLOOR = False    #床についているかどうか

    def __init__(self):
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