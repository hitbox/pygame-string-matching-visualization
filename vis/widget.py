import pygame as pg

class Widget(pg.sprite.Sprite):

    def __init__(self, text, inflate=(20, 20), minsize=None, border=None, **position):
        if border is None:
            border = engine.text_color
        super().__init__()
        self.image = engine.smalltext(text, minsize=minsize, border=border, inflate=inflate)
        self.rect = self.image.get_rect(**position)


from .engine import engine
