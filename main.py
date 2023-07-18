from typing import Any
from random import randint, random
import pygame as py

from engine.game_engine import Pygame
from engine.color import Color
from engine.game_objects import IGameObject
from engine.game_objects.modules import IAnimationModule, ICollisionModule
from engine.image import SpriteSheet
from engine.ui.text import TypeWriterText
from engine.map import LoopingMap

from src.player.player import Player


class UI_NPC_Text(TypeWriterText):
    def __init__(self, game: Pygame = None):
        super().__init__("We need to push forward! We need to push forward!", (200, 200, 200), game.fonts["8bit"], (135, 590), 10, game=game)


class UI_NPC_Text_Box(IGameObject):
    def __init__(self, game: Pygame = None):
        super().__init__("ui", game)
        self.pos = (120, 577)
        self.add_layer(f"{self.game.game_dir}\\data\\images\\ui\\ui_npc_text_box.png")
        self.rect = self.get_layer_image(0).get_rect(topleft=self.pos)

class UI_NPC_Box(IGameObject):
    def __init__(self, game: Pygame = None):
        super().__init__("ui", game)
        self.pos = (10, 665)
        # self.add_layer(f"{self.game.game_dir}/data/images/npc_board.png")
        self.add_layer(py.Surface((100, 100), flags=py.SRCALPHA))
        self.add_layer(py.Surface((100, 100), flags=py.SRCALPHA))
        self.add_layer(py.Surface((100, 100), flags=py.SRCALPHA))
        # self.add_layer(f"{self.game.game_dir}/data/images/npc_box.png")
        self.npc = ""
        self.npcs = {
            "red": py.image.load(f"{self.game.game_dir}/data/images/ui/npcs/red_npc.png")
        }
        self.anim_atlas = SpriteSheet(f"{self.game.game_dir}/data/images/ui/noise_atlas.png", 100, 100).get_image_array()
        self.rect = self.get_layer_image(1).get_rect(bottomleft=self.pos)

        self.set_module("animation", IAnimationModule(self, False))
        self.get_module("animation").add_animation_by_dict(
            "noise",
            {
                "layer": 1,
                "frames": [self.anim_atlas[0], self.anim_atlas[1], self.anim_atlas[2], self.anim_atlas[3],
                           self.anim_atlas[4], self.anim_atlas[5], self.anim_atlas[6], self.anim_atlas[7]],
                "frame_time": 40,
                "loop": False,
                "callback": self.noise_anim_ended
            }
        )
        
        self.get_module("animation").add_animation_by_dict(
            "noise_reversed",
            {
                "layer": 1,
                "frames": [self.anim_atlas[7], self.anim_atlas[6], self.anim_atlas[5], self.anim_atlas[4],
                           self.anim_atlas[3], self.anim_atlas[2], self.anim_atlas[1], self.anim_atlas[1]],
                "frame_time": 40,
                "loop": False,
                "callback": self.noise__reversed_anim_ended
            }
        )
        self.text = UI_NPC_Text(self.game)
        self.border = UI_NPC_Text_Box(self.game)
        self.game.objects.add("ui_npc_text", self.text)
        self.game.objects.add("ui_npc_text_box", self.border)
        self.get_module("animation").should_animate = True
        self.get_module("animation").play("noise")

    def noise_anim_ended(self):
        self.npc = "red"
        if self.npc != "":
            self.set_layer(self.npcs[self.npc], layer_id=0)
            self.set_layer(self.anim_atlas[8], layer_id=1)

        
    def noise__reversed_anim_ended(self):
        self.npc = ""
        self.set_layer(py.Surface((100, 100), py.SRCALPHA), layer_id=0)
        self.set_layer(py.Surface((100, 100), py.SRCALPHA), layer_id=1)


class UI_BG(IGameObject):
    def __init__(self, game=None):
        super().__init__("ui", game)
        self.pos = (0, 675)
        self.add_layer(f"{self.game.game_dir}/data/images/ui_bg.png")
        self.rect = self.get_layer_image(0).get_rect(bottomleft=self.pos)



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
    def __init__(self, group: str = "handler", game: Pygame = None):
        super().__init__(group, game)
        self.spawn_timing = 2000
        self.last_spawn_time = self.game.time

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.last_spawn_time + self.spawn_timing <= self.game.time:
            self.game.objects.add(f"rock_{randint(0, 999999)}", Rock(self.game))
            self.last_spawn_time = self.game.time
        return super().update(*args, **kwargs)


# MINIMAL RUNNING EXAMPLE #
# Main Game Engine Object #
class Game(Pygame):
    def __init__(self):
        super(Game, self).__init__(1200, 675, "Space Game", fps_target=60)
        self.add_group("handler")
        self.add_group("map")
        self.add_group("player")
        self.add_group("player_projectile")
        self.add_group("env")
        self.add_group("enemy")
        self.add_group('ui')
        self.fonts["8bit"] = self.get_font("8-BIT WONDER.ttf", 17)
        # SETUP GAME AXIS CONTROLS (IControlModule().get_axis("move_left"))
        self.axis = {'move_left': {py.K_a: -1, py.K_d: 1}, 'move_up': {py.K_w: -1, py.K_s: 1}}
        py.event.set_grab(True)
        py.mouse.set_pos((100, self.screen.get_height() / 2))
        py.mouse.set_visible(False)
        self.load_data()
        self.start_game_loop()

    def load_data(self):
        super(Game, self).load_data() # Required to set the base dir of the game for easy access in objects without recalculating where to split the path (self.game_dir)
        self.objects['map'] = LoopingMap(self, "data/images/background.png", [50, 0]) # Looping map uses the images size to calculate its looping. You may need to rescale your image to fit your game area (Window scaling will handle it after as long as it covers the initial screen). Supports vertical or horizontal but not both (Hopefully in future revisions)
        self.objects["player"] = Player((0, self.screen.get_height() / 2), self) # Adds a GameObject to the ObjectHandler so that update and draw calls are triggered correctly
        self.objects.add("rock_spawner", RockSpawner(game=self))
        self.objects["ui_bg"] = UI_BG(self)
        self.objects['ui_npc_box'] = UI_NPC_Box(self)
        # self.objects['ui_npc_text'] = UI_NPC_Text(self)

    def draw(self):
        self.screen.fill(Color(1, 1, 1, 1).RGB) # self.screen.fill((255, 255, 255)). Color class is used mostly for storing colors to easily recall but may get more features later
        super(Game, self).draw() # Required to call the draw function for registered objects
        # UNCOMMENT FOR RECT DEBUGGING
        if self.debug:
            for group in self.groups.keys():
                for sprite in self.groups[group]:
                    self.debug.debug_collision(sprite)
                        
                        
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
                if event.key == py.K_c: self.debug.set_debug(not self.debug._debug)
                if event.key == py.K_p:
                    npc_ui = self.objects.get("ui_npc_box")
                    if npc_ui.npc == "":
                        npc_ui.get_module("animation").play("noise")
                    else:
                        self.objects["ui_npc_box"].get_module("animation").play("noise_reversed")
                if event.key == py.K_ESCAPE:
                    self.quit()


if __name__ == '__main__':
    g = Game()
