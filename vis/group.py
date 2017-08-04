import pygame as pg

class Group(pg.sprite.Group):

    def __init__(self, *sprites, **position):
        super().__init__(*sprites)
        if position:
            self.position(**position)

    def position(self, widths=sum, heights=max, **rectkwargs):
        gestalt = pg.Rect(min(sprite.rect.left for sprite in self),
                          min(sprite.rect.top for sprite in self),
                          widths(sprite.rect.width for sprite in self),
                          heights(sprite.rect.width for sprite in self))
        for sprite in self:
            sprite.rect.move(-gestalt.x - sprite.rect.x, -gestalt.y - sprite.rect.y)


class NeedleLetters(Group):

    def __init__(self, *sprites, **position):
        super().__init__(*sprites, **position)
        self.originals = {sprite: sprite.rect.copy() for sprite in self}

    def update(self, state):
        if state is None:
            return
        if 'offset' in state:
            offset = state['offset']
            width = None
            for sprite in self:
                original = self.originals[sprite]
                if width is None:
                    width = sprite.rect.width
                sprite.rect = original.move(offset * width, 0)
