# MINIMAL RUNNING EXAMPLE #
# Main Game Engine Object #
import pygame as py

from engine.color import Color
from engine.game_engine import Pygame
from engine.game_objects import IGameObject
from engine.game_objects.modules import IAnimationModule, IControlModule
from engine.math import Vector2
from engine.image import SpriteSheet
from engine.map import TileMap


# Player Object #
class Player(IGameObject):
    def __init__(self, pos: tuple[int, int], game: 'engine.game_objects.IGameObject'):
        super(Player, self).__init__('player', game)
        self.modules["control"] = IControlModule(self, callback=self.callback_input_tick)

        self.pos = pos
        self.move_speed = 3
        self.sprite_sheet = SpriteSheet(f"{self.game.game_dir}\\data\\images\\player\\player_atlas.png", 29, 39).get_image_array()
        self.add_layer(self.sprite_sheet[4])
        self.rect = self.get_layer_image(0).get_rect(center=self.pos)
        self.debug = True

    def callback_input_tick(self):
        up_vel = self.get_module("control").get_axis("move_up") * self.move_speed
        left_vel = self.get_module("control").get_axis("move_left") * self.move_speed
        self.pos = (self.rect.centerx + left_vel, self.rect.centery + up_vel)

    def update(self, *args, **kwargs):
        newPos = Vector2.get_diff_tuple(self.rect.center, self.pos) if self.rect.center > self.pos else Vector2.get_diff_tuple(self.pos, self.rect.center)
        self.pos += newPos * 0.1
        self.rect.center = self.pos
        super(Player, self).update()


class Game(Pygame):
    def __init__(self):
        super(Game, self).__init__(704, 448, "Dungeon Game", fps_target=60)
        self.add_group("map")
        self.add_group("player")
        # SETUP GAME AXIS CONTROLS (IControlModule().get_axis("move_left"))
        self.axis = {'move_left': {py.K_a: -1, py.K_d: 1}, 'move_up': {py.K_w: -1, py.K_s: 1}}
        self.load_data()
        self.start_game_loop()

    def load_data(self):
        super(Game, self).load_data() # Required to set the base dir of the game for easy access in objects without recalculating where to split the path (self.game_dir)
        self.add_object("map", TileMap(self, "data\\maps\\r0_c0.tmx"))
        self.add_object('player', Player((self.window_size.x / 2, self.window_size.y / 2), self))

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