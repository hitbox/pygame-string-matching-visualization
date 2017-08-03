import argparse
import pygame as pg

import logic

class engine:

    clock = None
    framerate = 60
    screen = None

    small_font = None
    text_color = (200,200,200)

    @classmethod
    def init(cls):
        pg.init()

        cls.clock = pg.time.Clock()
        cls.screen = pg.display.set_mode((800, 600))
        cls.rect = cls.screen.get_rect()

        cls.small_font = pg.font.SysFont('Consolas', 20)

    @classmethod
    def tick(cls):
        return cls.clock.tick(cls.framerate)

    @classmethod
    def smalltext(cls, text, color=None, border=None, inflate=None, minsize=None):
        if color is None:
            color = cls.text_color

        if minsize is None:
            minsize = (0, 0)

        image = cls.small_font.render(text, True, color)
        rect = image.get_rect()

        resize = image.get_rect()
        resize.size = max((rect.width, minsize[0])), max((rect.height, minsize[1]))

        if (rect.width >= minsize[0]
                and rect.height <= minsize[1]):
            resize = None

        if inflate or resize:
            if resize is None:
                resize = image.get_rect()
            if inflate is None:
                inflate = (0, 0)

            inflated = resize.inflate(*inflate)

            inflated.topleft = (0, 0)
            result = pg.Surface(inflated.size, pg.SRCALPHA)
            result.blit(image, image.get_rect(center=inflated.center))
            image = result
            rect = image.get_rect()

        if border:
            pg.draw.rect(image, border, rect, 1)

        return image


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


class Letter(pg.sprite.Sprite):

    def __init__(self, type, letter, index, **position):
        super().__init__()
        self.type = type
        self.index = index
        self.image = engine.smalltext(letter)
        self.rect = self.image.get_rect(**position)


class Widget(pg.sprite.Sprite):

    def __init__(self, text, inflate=(20, 20), minsize=None, border=engine.text_color, **position):
        super().__init__()
        self.image = engine.smalltext(text, minsize=minsize, border=border, inflate=inflate)
        self.rect = self.image.get_rect(**position)


class Textbox(Widget):

    def __init__(self, text='', **kwargs):
        kwargs.setdefault('minsize', (250,0))
        super().__init__(text, **kwargs)
        #TODO: make editable


class Button(Widget):

    def __init__(self, text, inflate=(20, 20), **position):
        super().__init__(text, inflate=inflate, **position)
        #TODO: clickable


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


def lettersprites(type, s, left, top):
    width = None
    for index, letter in enumerate(s):
        letter = Letter(type, letter, index, top=top)
        if width is None:
            width = letter.rect.width
        letter.rect.left = left + (index * width)
        yield letter

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


def loop(algoritm_class=logic.BoyerMoore):

    algoritm = algoritm_class('ABCDABD', 'ABC ABCDAB ABCDABCDABDE')

    buttons = pg.sprite.Group(
        Button('Step', topright=(engine.rect.right-20, 20)),
    )

    haystackletters = pg.sprite.Group(
        tuple(lettersprites('haystack', algoritm.haystack, 100, 100)),
    )

    needleletters = NeedleLetters(
        tuple(lettersprites('needle', algoritm.needle, 100, 120)),
        center = engine.rect.center,
    )
    letters = pg.sprite.Group(haystackletters, needleletters)

    stategroup = pg.sprite.Group(
        JayPointer(midright=engine.rect.midright),
    )
    allgroup = pg.sprite.Group(buttons, letters, stategroup)

    stateiter = algoritm.search()
    state = next(stateiter)

    NEXTSTATE = pg.USEREVENT

    pg.time.set_timer(NEXTSTATE, 1000)

    running = True
    while running:
        dt = engine.tick()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_q):
                    pg.event.post(pg.event.Event(pg.QUIT))
            elif event.type == NEXTSTATE:
                state = next(stateiter, None)
                if state:
                    if state.get('success', False):
                        allgroup.add(Textbox('FOUND!', center=engine.rect.center))

        buttons.update()
        haystackletters.update()
        needleletters.update(state)
        stategroup.update(letters, state)

        engine.screen.fill((0,0,0))
        allgroup.draw(engine.screen)

        pg.display.flip()

def main():
    """
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    args = parser.parse_args()

    engine.init()
    loop()

if __name__ == '__main__':
    main()
