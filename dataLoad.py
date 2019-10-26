import pygame
from pygame.locals import *

def split_images(filePath, size=32, number=2, flip=None):
    '''64x32のキャラクターイメージを32x32の2枚のイメージに分割
    分割したイメージを格納したリストを返す'''
    imageList = []
    try:
        image = pygame.image.load(filePath)
    except pygame.error as message:
        raise SystemExit ("Cannot load image :" + " " + filePath)
    if flip is not None:
        if flip == 1:
            image = pygame.transform.flip(image, 1, 0)
        elif flip == 2:
            image = pygame.transform.flip(image, 0, 1)
    for i in range(0, size*number, size):
        surface = pygame.Surface((size, size))
        surface.blit(image, (0, 0), (i, 0, size, size))
        surface.set_colorkey(surface.get_at((0, 0)), RLEACCEL)
        surface.convert()
        imageList.append(surface)
    return imageList

def load_image(filePath, colorkey=None):
    '''画像をロードして画像と矩形を返す'''
    try:
        image = pygame.image.load(filePath)
    except pygame.error as message:
        raise SystemExit ("Cannot load image :" + " " + filePath)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def load_sound(filePath):
    '''効果音をロードしてSoundオブジェクトを返す'''
    return pygame.mixer.Sound(filePath)