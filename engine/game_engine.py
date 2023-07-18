#!/usr/bin/env python
# -*- coding=utf-8 -*-

import traceback
import sys
from os import path
from collections import UserDict

import pygame as py

exc_info = None

from engine.math.vector import Vector2
from engine.debug import DebugHandler

class SpriteGroup(py.sprite.LayeredUpdates):
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        game = None
        _map = None
        for spr in self.sprites():
            if game is None:
                game = spr.game
            if _map is None:
                _map = game.get_object("map")
            if hasattr(spr, "draw_sprite"):
                if spr.draw_sprite:
                    rec = spritedict[spr]
                    
                    if _map is not None:
                        if _map.follow_camera:
                            new_rect = surface_blit(spr.draw()[0], _map.camera.apply(spr))
                        else:
                            new_rect = surface_blit(*spr.draw())
                    else:
                        new_rect = surface_blit(*spr.draw())
                    if rec is init_rect:
                        dirty_append(new_rect)
                    else:
                        if new_rect.colliderect(rec):
                            dirty_append(new_rect.union(rec))
                        else:
                            dirty_append(new_rect)
                            dirty_append(rec)
                    spritedict[spr] = new_rect
        return dirty


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
    CLOCK = py.time.Clock()
    def __init__(self, width, height, title, fps_target=60):
        py.init()
        py.font.init()
        self.window_size = Vector2(width, height)
        self.screen = py.display.set_mode(self.window_size, py.RESIZABLE | py.SCALED)
        py.display.set_caption(title)
        self.fps_target = fps_target
        self.fps = self.CLOCK.get_fps()
        self.frame_time = py.time.get_ticks()
        self.axis = {}
        self.state = "init"
        self.objects = ObjectHandler()
        self.groups = {'all_sprites': SpriteGroup()}
        self.fonts = {'default': py.font.Font(path.join(path.dirname(__file__), f'ui\\i_pixel_u.ttf'), 25)}
        self.running = True
        self.game_dir = ""
        self.debug = DebugHandler(False, self)
        self.allow_fullscreen = True
        self.full_screen_key = py.K_F11
        self._full_screen_pressed = 0
        self.delta_time = 0

    @staticmethod
    def get_font(name: str, size: int = 25): return py.font.Font(path.join(path.dirname(__file__).split('\\engine')[0], f'data\\fonts\\{name}'), size)
    @staticmethod
    def render_display(): py.display.update()

    @staticmethod
    def quit():
        py.quit()
        try:
            exit()
        except Exception:
            pass

    @property
    def time(self) -> int: return py.time.get_ticks()
    
    def load_data(self): self.game_dir = path.dirname(__file__).split('\\engine')[0]        
    def toggle_debug(self): self.debug.set_debug(not self.debug._debug)
    def set_state(self, state: str): self.state = state
    def add_group(self, group_name: str): self.groups[group_name] = SpriteGroup()
    def add_object(self, key: str, obj: 'engine.game_objects.IGameObject'): self.objects[key] = obj
    def get_object(self, key: str): return self.objects[key]
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
        self.CLOCK.tick(self.fps_target)
        self.fps = self.CLOCK.get_fps()
        self.delta_time = abs(self.time - self.frame_time) / 1000
        self.frame_time = py.time.get_ticks()
        if self.allow_fullscreen:
            if self._full_screen_pressed != py.key.get_pressed()[self.full_screen_key]:
                self._full_screen_pressed = py.key.get_pressed()[self.full_screen_key]
                if self._full_screen_pressed:
                    py.display.toggle_fullscreen()
        for o in dict(self.objects):
            try:
                self.objects[o].update(self.state)
            except KeyError:
                pass
            except Exception:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
