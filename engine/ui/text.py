import pygame as py

from engine.game_objects.game_object import GameObject
from engine.color import Color

# Default Text Object #

class Text(GameObject):
    def __init__(self, text, 
                 color: tuple = Color(1, 1, 1, 0).RGB, 
                 font: py.font.Font = None,
                 pos: tuple = (0,0),
                 game = None,
                 group='ui'
                ):
        super(Text, self).__init__(group, game)
        if font is None:
            font = py.font.Font("engine/ui/i_pixel_u.ttf", 25)

        self.font, self.text, self.color, self.pos = font, text, color, pos
        self.update_text(str(self.text))

    def update(self): pass

    def update_text(self, text):
        self.text = text
        self.image = self.font.render(text, 1, self.color)
        self.rect = self.image.get_rect(center=self.pos)
