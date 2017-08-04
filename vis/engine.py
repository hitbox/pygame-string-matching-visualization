import pygame as pg

class engine:

    clock = None
    framerate = 60
    screen = None

    small_font = None
    text_color = (200,200,200)

    state = None

    callbacks = None

    @classmethod
    def init(cls, state):
        pg.init()

        cls.clock = pg.time.Clock()
        cls.screen = pg.display.set_mode((800, 600))
        cls.rect = cls.screen.get_rect()

        cls.small_font = pg.font.SysFont('Consolas', 40)

        cls.callbacks = {}
        cls.state = state
        cls.state.init()

    @classmethod
    def register(cls, type, func):
        cls.callbacks[type] = func

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

    @classmethod
    def run(cls):
        running = True
        while running:
            dt = engine.tick()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type in cls.callbacks:
                    cls.callbacks[event.type](event)
            cls.state.update()
            pg.display.flip()
