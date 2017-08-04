import pygame as pg

class Letter(pg.sprite.Sprite):

    def __init__(self, type, letter, index, **position):
        super().__init__()
        self.type = type
        self.index = index
        self.image = engine.smalltext(letter)
        self.rect = self.image.get_rect(**position)

from .engine import engine
