import pygame as pg

def lettersprites(type, s, left, top):
    width = None
    for index, letter in enumerate(s):
        letter = Letter(type, letter, index, top=top)
        if width is None:
            width = letter.rect.width
        letter.rect.left = left + (index * width)
        yield letter

class State:
    pass


NEXTSTATE = pg.USEREVENT

class VisState(State):

    def __init__(self, pattern, text, algoritm_class=None):
        if algoritm_class is None:
            algoritm_class = logic.BoyerMoore
        self.algoritm = algoritm_class(pattern, text)

    def init(self):
        self.buttons = pg.sprite.Group(
            Button('Step', topright=(engine.rect.right-20, 20)),
        )

        self.haystackletters = pg.sprite.Group(
            tuple(lettersprites('haystack', self.algoritm.haystack, 100, 100)),
        )

        top = self.haystackletters.sprites()[0].rect.bottom

        self.needleletters = NeedleLetters(
            tuple(lettersprites('needle', self.algoritm.needle, 100, top)),
            center = engine.rect.center,
        )
        self.letters = pg.sprite.Group(self.haystackletters, self.needleletters)

        self.stategroup = pg.sprite.Group(
            JayPointer(midright=engine.rect.midright),
        )
        self.allgroup = pg.sprite.Group(self.buttons, self.letters, self.stategroup)

        self.stateiter = self.algoritm.search()
        self.state = next(self.stateiter)

        engine.register(pg.KEYDOWN, self.keydown)

        pg.time.set_timer(NEXTSTATE, 1000)
        engine.register(NEXTSTATE, self.nextstate)

    def keydown(self, event):
        if event.key in (pg.K_ESCAPE, pg.K_q):
            pg.event.post(pg.event.Event(pg.QUIT))

    def nextstate(self, event):
        self.state = next(self.stateiter, None)
        if self.state:
            success = self.state.get('success')
            if success:
                self.allgroup.add(Textbox('FOUND!', center=engine.rect.center))
            elif success is not None:
                self.allgroup.add(Textbox('NOPE!', center=engine.rect.center))

    def update(self):
        self.buttons.update()
        self.haystackletters.update()
        self.needleletters.update(self.state)
        self.stategroup.update(self.letters, self.state)

        engine.screen.fill((0,0,0))
        self.allgroup.draw(engine.screen)


from . import logic
from .button import Button
from .engine import engine
from .group import NeedleLetters
from .letter import Letter
from .pointer import JayPointer
from .textbox import Textbox
