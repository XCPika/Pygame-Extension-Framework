import pygame as py

from engine.game_objects.game_object import GameObject
from engine.color import Color

# Default Text Object #

class Text(GameObject):
    def __init__(self, text, 
                 color: tuple = Color(1, 1, 1, 1).RGBA, 
                 font: py.font.Font = None,
                 pos: tuple = (0,0),
                 game = None,
                 group='ui'
                ):
        super(Text, self).__init__(group, game)
        if font is None:
            font = py.font.Font("engine/ui/i_pixel_u.ttf", 25)

        self.font, self.text, self.color, self.pos = font, text, color, pos
        self.add_layer(self.draw_text())
        self.rect = self.get_layer_image(0).get_rect(topleft=self.pos)

    def draw_text(self):
        font = self.font.render(self.text, 1, self.color)
        surface = py.Surface(font.get_size(), flags=py.SRCALPHA)
        surface.blit(font, (0, 0))
        return surface

    def update_text(self, text):
        self.text = text    
        self.set_layer(self.draw_text(), 0)
        self.rect = self.get_layer_image(0).get_rect(topleft=self.pos)