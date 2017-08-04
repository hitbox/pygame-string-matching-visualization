from . import widget

class Button(widget.Widget):

    def __init__(self, text, inflate=(20, 20), **position):
        super().__init__(text, inflate=inflate, **position)
        #TODO: clickable
