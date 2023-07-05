import pygame as py
from os import path
from collections import UserDict

from engine.math.vector import Vector2


# Object Handler #
class ObjectHandler(UserDict):
    def __setitem__(self, key, obj):
        super().__setitem__(key, obj)
        obj.set_object_key(key)

    def __delitem__(self, key):
        try:
            self[key].kill()
        except KeyError:
            pass
        super().__delitem__(key)


# Pygame Basic Game Engine #
class Pygame:
    def __init__(self, width, height, title, fps_target=60):
        py.init()
        py.font.init()
        self.windowSize = Vector2(width, height)
        self.screen = py.display.set_mode(self.windowSize, py.RESIZABLE | py.SCALED)
        py.display.set_caption(title)
        self.clock = py.time.Clock()
        self.fps_target = fps_target
        self.fps = self.clock.get_fps()
        self.time = py.time.get_ticks()
        self.axis = {}
        self.objects = ObjectHandler()
        self.groups = {'all_sprites': py.sprite.Group(), 'ui': py.sprite.Group(), 'none': py.sprite.Group()}
        self.fonts = {'default': py.font.Font(path.join(path.dirname(__file__), f'ui\\i_pixel_u.ttf'), 25)}
        self.running = True
        self.game_dir = ""
        self.debug = False
        self.allow_fullscreen = True
        self.full_screen_key = py.K_F11
        self._full_screen_pressed = 0

    @staticmethod
    def get_font(name): return py.font.Font(path.join(path.dirname(__file__).split('\\engine')[0], f'data\\fonts\\{name}.ttf'), 25)
    @staticmethod
    def render_display(): py.display.flip()
    def load_data(self): self.game_dir = path.dirname(__file__).split('\\engine')[0]

    @staticmethod
    def quit():
        py.quit()
        try:
            exit()
        except Exception:
            pass

    def draw(self):
        for o in self.groups:
            if o != "none":
                self.groups[o].draw(self.screen)

    def update(self):
        self.clock.tick(self.fps_target)
        self.fps = self.clock.get_fps()
        self.time = py.time.get_ticks()
        if self.allow_fullscreen:
            if self._full_screen_pressed != py.key.get_pressed()[self.full_screen_key]:
                self._full_screen_pressed = py.key.get_pressed()[self.full_screen_key]
                if self._full_screen_pressed:
                    py.display.toggle_fullscreen()
        for o in dict(self.objects):
            self.objects[o].update()
