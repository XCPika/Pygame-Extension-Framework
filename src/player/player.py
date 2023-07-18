"""
    Defines the main player ship class
"""
from __future__ import annotations
from random import random

import pygame as py

from engine.game_objects import IGameObject
from engine.image import SpriteSheet
from engine.game_objects.modules import IAnimationModule, ICollisionModule, IControlModule

from src.player.bullet import Bullet

# Player Object #
class Player(IGameObject):
    can_fire = True
    last_fire_time = -2000
    def __init__(self, pos: tuple, game: engine.game_engine.Pygame) -> None:
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