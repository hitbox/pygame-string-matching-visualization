from . import widget

class Textbox(widget.Widget):

    def __init__(self, text='', **kwargs):
        kwargs.setdefault('minsize', (250,0))
        super().__init__(text, **kwargs)
        #TODO: make editable
