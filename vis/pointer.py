import pygame as pg

class JayPointer(pg.sprite.Sprite):

    def __init__(self, **position):
        super().__init__()
        self.image = engine.smalltext('^')
        self.rect = self.image.get_rect(**position)

    def update(self, letters, state):
        if state is None or 'j' not in state:
            return
        for sprite in letters:
            if sprite.type == 'needle' and sprite.index == state['j']:
                self.rect.midtop = sprite.rect.midbottom
                break

from .engine import engine
