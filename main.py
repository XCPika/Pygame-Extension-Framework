from typing import Any
from random import randint, random
import pygame as py

from engine.game_engine import Pygame
from engine.color import Color
from engine.game_objects import IGameObject
from engine.game_objects.modules import IControlModule, IAnimationModule, ICollisionModule
from engine.image import SpriteSheet
from engine.ui.text import Text
from engine.map import LoopingMap


class UI_NPC_Text(Text):
    def __init__(self, game: Pygame = None):
        super().__init__("test", (125, 125, 125, 255), game.fonts["default"], (250, 600), game, 'ui')


class UI_NPC_Box(IGameObject):
    def __init__(self, game: Pygame = None):
        super().__init__("ui", game)
        self.pos = (10, 665)
        # self.add_layer(f"{self.game.game_dir}/data/images/npc_board.png")
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

class Bullet(IGameObject):
    def __init__(self, pos, game):
        super(Bullet, self).__init__("player_projectile", game)
        self.set_module("collision", ICollisionModule(self, True, self.callback_collision))
        self.get_module("collision").collision_groups = ["env", "enemy"]

        self.pos = pos
        self.vel = 2
        self.max_vel = 15
        self.accel = 4
        self.spawn_time = self.game.time
        self.add_layer(f"{self.game.game_dir}/data/images/bullet.png")
        self.rect = self.get_layer_image(0).get_rect(midleft=self.pos)
        self.mask = py.mask.from_surface(self.get_layer_image(0))

    def callback_collision(self, hit, group):
        hit.destroy()
        self.destroy()
    
    def update(self, *args, **kwargs) -> None:
        self.pos = (self.pos[0] + self.vel, self.pos[1])
        self.vel = min(self.vel + self.accel, self.max_vel)
        self.rect = self.get_layer_image(0).get_rect(midleft=self.pos)
        if self.spawn_time + 2000 <= self.game.time:
            self.destroy()
        return super(Bullet, self).update(args, kwargs)
    

# Player Object #
class Player(IGameObject):
    can_fire = True
    last_fire_time = -2000
    def __init__(self, pos: tuple, game: Pygame):
        super(Player, self).__init__('player', game)
        self.set_module("control", IControlModule(self, callback=self.callback_input_tick, allow_control=False)) # or self.modules['control'] = IControlModule(self, callback=self.callback_input_tick, allow_control=False) 
        self.set_module("animation", IAnimationModule(self))
        self.set_module("collision", ICollisionModule(self, True, self.callback_collision))
        self.get_module("collision").collision_groups = ["env", "enemy"]
        self.pos = pos 
        self.last_pos = (0, 0) # Used as part of animation logic (Not required)
        self.move_speed = 150

        self.sprite_sheet = SpriteSheet(f"{self.game.game_dir}/data/images/ship_00.png", 66, 38).get_image_array()
        self.add_layer(self.sprite_sheet[0])
        self.rect = self.get_layer_image(self.primary_layer).get_rect(center=self.pos)
        self.mask = py.mask.from_surface(self.get_layer_image(0))
        # Optionally: self.modules.get_module("animation").add_animation_by_json(file_location: str) file_location is relative to game_dir
        self.get_module("animation").add_animation_by_dict("engines_on",
            {   
                "layer": 0,
                "frames": [self.sprite_sheet[1]],
                "frame_time": 500,
                "loop": False,
                "callback": self.callback_engine_anim_ended
            }
        )
        self.modules["animation"].should_animate = True

    def callback_collision(self, hit, group):
        hit.destroy()

    def callback_engine_anim_ended(self):
        self.set_layer(self.sprite_sheet[0], layer_id=0)

    def callback_input_tick(self):
        self.last_pos = self.pos
        control = self.get_module("control")
        pos = (control.get_axis("move_left") * self.move_speed * self.game.delta_time, control.get_axis("move_up") * self.move_speed * self.game.delta_time)
        shoot = control.get_key(py.K_SPACE)
        if shoot:
            if self.last_fire_time + 500 <= self.game.time:
                self.game.objects.add(f"bullet_{random() * 999999}", 
                                    Bullet((self.pos[0] + 15, self.pos[1]), self.game)
                                    )
                self.last_fire_time = self.game.time
        self.pos = (self.pos[0] + pos[0], max(min(580, self.pos[1] + pos[1]), 0))

    def update(self, *args, **kwargs) -> None:
        state = args[0]
        if state != "start":
            self.get_module("control").allow_control = True
            if self.last_pos != self.pos:
                self.modules["animation"].play("engines_on")
        else:
            self.modules["animation"].play("engines_on")
            self.pos = (self.pos[0] + 1, self.pos[1])
            if self.pos[0] >= 100:
                self.game.state = "level_0"
                self.game.objects.get("ui_npc_box").get_module("animation").play("noise_reversed")
                
        self.rect = self.get_layer_image(0).get_rect(center=self.pos)
        super(Player, self).update(args, kwargs)


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
        for group in self.groups.keys():
            for sprite in self.groups[group]:
                if self.debug:
                    if sprite.debug:
                        if hasattr(sprite, "mask"):
                            if sprite.mask is not None:
                                self.screen.blit(sprite.mask.to_surface(), sprite.rect)
                        py.draw.rect(py.display.get_surface(), Color(1, 0, 0, 1).RGBA, sprite.rect, 1)
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
                if event.key == py.K_c: self.debug = not self.debug
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
