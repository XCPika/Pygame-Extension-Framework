
from __future__ import annotations

import pygame as py

from engine.game_objects import IGameObject
from engine.game_objects.modules import  ICollisionModule


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