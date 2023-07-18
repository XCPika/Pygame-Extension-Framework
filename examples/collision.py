from random import random, randint

import pygame as py

from engine.game_engine import Pygame
from engine.color import Color
from engine.game_objects import IGameObject
from engine.game_objects.modules import IControlModule, ICollisionModule


# Rock Object #
class Rock(IGameObject):
    def __init__(self, game: Pygame):
        super(Rock, self).__init__('env', game)
        self.set_module("collision", ICollisionModule(self, False))
        self.pos = (self.game.screen.get_width(), randint(0, self.game.screen.get_height()))
        self.vel = (randint(-2,-1), randint(-1, 1) * (random() * 0.5))
        spr = py.image.load(f"{self.game.game_dir}/data/images/rock.png").convert_alpha()
        scale = max(25, random() * 48)
        spr = py.transform.scale(spr, (scale, scale))
        spr = py.transform.rotate(spr, randint(-25, 25))
        self.add_layer(spr)
        self.rect = self.get_layer_image(self.primary_layer).get_rect(center=self.pos)
        self.mask = py.mask.from_surface(self.get_layer_image(0))

    def update(self, *args, **kwargs) -> None:
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.rect = self.get_layer_image(0).get_rect(center=self.pos)
        super(Rock, self).update()


class RockSpawner(IGameObject):
    def __init__(self, game: Pygame = None):
        super().__init__("handler", game)
        self.spawn_timing = 2000
        self.last_spawn_time = self.game.time

    def update(self, *args, **kwargs) -> None:
        if self.last_spawn_time + self.spawn_timing <= self.game.time:
            self.game.objects.add(f"rock_{randint(0, 999999)}", Rock(self.game))
            self.last_spawn_time = self.game.time
        return super().update(*args, **kwargs)


# Player Object #
class Player(IGameObject):
    def __init__(self, pos: tuple, game: Pygame):
        super(Player, self).__init__('player', game)
        self.modules.set_module("control", IControlModule(self, callback=self.callback_input_tick)) # or self.modules['control'] = IControlModule(self, callback=self.callback_input_tick) 
        self.set_module("collision", ICollisionModule(self, True, self.callback_collision))
        self.get_module("collision").collision_groups = ["env"]

        self.add_layer(py.image.load(f"{self.game.game_dir}/data/images/player.png"))
        self.mask = py.mask.from_surface(self.get_layer_image(0)) # Optional. This allows to masked collisions
        self.pos = pos 
        self.rect = self.get_layer_image(0).get_rect(center=self.pos)

    def callback_collision(self, hit, group):
        hit.destroy()

    def callback_input_tick(self):
        self.pos = self.modules["control"].get_mouse_pos()

    def update(self, *args, **kwargs):
        self.rect = self.get_layer_image(0).get_rect(center=self.pos)
        super(Player, self).update()


# CONTROL EXAMPLE #
# Main Game Engine Object #
class Game(Pygame):
    def __init__(self):
        super(Game, self).__init__(1280, 720, "Space Game", fps_target=60)
        self.add_group("player") # The order groups are registered in is what pygame uses as layer render order. First added is first rendered (Put things like map groups in first)
        self.add_group("env")
        self.add_group("handler")
        # SETUP GAME AXIS CONTROLS (IControlModule().get_axis("move_left"))
        self.axis = {'move_left': {py.K_a: -1, py.K_d: 1}, 'move_up': {py.K_w: -1, py.K_s: 1}}
        self.load_data()
        self.start_game_loop()

    def load_data(self):
        super(Game, self).load_data() # Required to set the base dir of the game for easy access in objects without recalculating where to split the path (self.game_dir)
        self.objects["player"] = Player((self.screen.get_width() / 2, self.screen.get_height() / 2), self) # Adds a GameObject to the ObjectHandler so that update and draw calls are triggered correctly
        self.objects["rock_spawner"] = RockSpawner(self)

    def draw(self):
        self.screen.fill(Color(1, 1, 1, 1).RGB) # self.screen.fill((255, 255, 255)). Color class is used mostly for storing colors to easily recall but may get more features later
        super(Game, self).draw() # Required to call the draw function for registered objects
        # UNCOMMENT FOR RECT DEBUGGING
        # if self.debug:
        #     for group in self.groups.keys():
        #         for sprite in self.groups[group]:
        #             self.debug.debug_collision(sprite)
        super(Game, self).render_display() # Required to call the render update of the display (py.display.flip())

    def update(self):
        super(Game, self).update()
        for event in py.event.get():
            # COMMENT TO REMOVE MANUAL WINDOW RESIZING SUPPORT
            if event.type == py.VIDEORESIZE:
                self.windowSize = (event.w, event.h)
                py.display._resize_event(event)
            if event.type == py.QUIT:
                self.quit()
            if event.type == py.KEYDOWN:
                # UNCOMMENT TO TOGGLE DEBUGGING
                # if event.key == py.K_c: 
                #     self.debug.set_debug(not self.debug._debug)
                if event.key == py.K_ESCAPE:
                    self.quit()


if __name__ == '__main__':
    g = Game()
