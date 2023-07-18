import pygame as py

from engine.color import Color
from engine.ui.text.text import Text


class TypeWriterText(Text):
    def __init__(self,
                 text, 
                 color: tuple = Color(1, 1, 1, 1).RGBA, 
                 font: py.font.Font = None,
                 pos: tuple = (0,0),
                 delay: int = 0,
                 game = None,
                 ):
        super(TypeWriterText, self).__init__("", color, font, pos, game, 'ui')
        self.display_text = text
        self.cur_char = 0
        self.last_time = 0
        self.delay = delay

    def update(self, *args, **kwargs) -> None:
        if self.display_text != self.text:
            if self.last_time + self.delay <= self.game.time:
                print(self.display_text[self.cur_char:self.cur_char + 1])
                self.text += self.display_text[self.cur_char:self.cur_char + 1]
                self.set_layer(self.draw_text(), (0, 0), 0)
                self.cur_char += 1
                self.last_time = self.game.time

    def update_text(self, text):
        self.text = ""
        self.display_text = text
        self.set_layer(self.draw_text(), 0)
        self.rect = self.get_layer_image(0).get_rect(topleft=self.pos)

    def draw_text(self):
        font = self.font.render(self.text, 1, self.color, wraplength=300)
        surface = py.Surface(font.get_size(), flags=py.SRCALPHA)
        surface.blit(font, (0, 0))
        return surface

    