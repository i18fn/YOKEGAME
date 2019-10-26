import pygame
import dataLoad
import os

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, filePath, size):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = dataLoad.load_image("Data/Block.bmp")
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Map:
    GS = 32
    def __init__(self, filename, all, SCR_RECT, GS=32):
        self.loadMap(filename)
        self.all = all
        self.SCR_RECT = SCR_RECT
        self.surface = pygame.Surface((self.col*self.GS, self.row*self.GS)).convert()

    def draw(self):
        self.surface.fill((255, 255, 255))
        self.all.draw(self.surface)

    def update(self, screen, obj=None):
        self.all.update()
        self.scroll(screen, obj)

    def loadMap(self, filename):
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
                    Block((j*self.GS, i*self.GS), "Data/Block.bmp", 32)
                #if map[i][j] == '2':
                #if map[i][j] == '3':
                #if map[i][j] == '4':
                #if map[i][j] == '5':     
    
    def scroll(self, screen, obj):
        '''画面のスクロール処理'''
        offsetx, offsety = self.calc_offset(obj) 
        #画面の端ではスクロールしない
        if offsetx < 0:
            offsetx = 0
        elif offsetx > self.width - self.SCR_RECT.width:
            offsetx = self.width - self.SCR_RECT.width

        if offsety < 0:
            offsety = 0
        elif offsety > self.height - self.SCR_RECT.height:
            offsety = self.height - self.SCR_RECT.height

        #マップの一部を画面に描画
        screen.blit(self.surface, (0, 0), (offsetx, offsety, self.SCR_RECT.width, self.SCR_RECT.height))

    def calc_offset(self, obj):
        '''オフセット(自機を中心としたときの画面の左上の座標)の計算'''
        offsetx = obj.rect.topleft[0] - self.SCR_RECT.width//2
        offsety = obj.rect.topleft[1] - self.SCR_RECT.height//2
        return offsetx, offsety
                          

