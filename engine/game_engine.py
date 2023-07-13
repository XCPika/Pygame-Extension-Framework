import pygame as py
import traceback
import sys
from os import path
from collections import UserDict

exc_info = None

from engine.math.vector import Vector2

class SpriteGroup(py.sprite.LayeredUpdates):
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            if hasattr(spr, "draw_sprite"):
                if spr.draw_sprite:
                    rec = spritedict[spr]
                    newrect = surface_blit(*spr.draw())
                    if rec is init_rect:
                        dirty_append(newrect)
                    else:
                        if newrect.colliderect(rec):
                            dirty_append(newrect.union(rec))
                        else:
                            dirty_append(newrect)
                            dirty_append(rec)
                    spritedict[spr] = newrect
        return dirty

# Object Handler #
class ObjectHandler(UserDict):
    def add(self, key, obj): self.__setitem__(key, obj)
        
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
        self.state = "init"
        self.objects = ObjectHandler()
        self.groups = {'all_sprites': SpriteGroup()}
        self.fonts = {'default': py.font.Font(path.join(path.dirname(__file__), f'ui\\i_pixel_u.ttf'), 25)}
        self.running = True
        self.game_dir = ""
        self.debug = False
        self.allow_fullscreen = True
        self.full_screen_key = py.K_F11
        self._full_screen_pressed = 0
        self.delta_time = 0

    def add_group(self, group_name: str): self.groups[group_name] = SpriteGroup()

    @staticmethod
    def get_font(name: str): return py.font.Font(path.join(path.dirname(__file__).split('\\engine')[0], f'data\\fonts\\{name}.ttf'), 25)
    @staticmethod
    def render_display(): py.display.update()
    def load_data(self): self.game_dir = path.dirname(__file__).split('\\engine')[0]

    @staticmethod
    def quit():
        py.quit()
        try:
            exit()
        except Exception:
            pass

    def start_game_loop(self):
        self.state = "start"
        while self.running:
            self.update()
            self.draw()

    def draw(self):
        for o in self.groups:
            if o != "none":
                self.groups[o].draw(self.screen)

    def update(self):
        self.clock.tick(self.fps_target)
        self.fps = self.clock.get_fps()
        self.delta_time = abs(py.time.get_ticks() - self.time) / 1000
        self.time = py.time.get_ticks()
        if self.allow_fullscreen:
            if self._full_screen_pressed != py.key.get_pressed()[self.full_screen_key]:
                self._full_screen_pressed = py.key.get_pressed()[self.full_screen_key]
                if self._full_screen_pressed:
                    py.display.toggle_fullscreen()
        for o in dict(self.objects):
            try:
                self.objects[o].update(self.state)
            except Exception as err:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
