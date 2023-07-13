from typing import Any
import pygame as py

from engine.game_objects.game_object import IGameObject
from engine.helpers import get_truth


class LoopingMap(IGameObject):
    def __init__(self, game, file: str = "map.png", speed:list=[0.5, 0]):
        super(LoopingMap, self).__init__("map", game)
        self.file = file
        self.background = py.image.load(f"{self.game.game_dir}/{file}").convert_alpha()
        self.add_layer(self.background)
        self.add_layer(self.background)
        self.rect = self.get_layer_image(0).get_rect()
        self.speed = speed
        self.bg_pos = [0, 0]
        if speed[0] < 0 and speed[0] < speed[1]:
            self.axis = 0
            self.dir = 0
        elif speed[0] > 0 and speed[0] > speed[1]:
            self.axis = 0
            self.dir = 1
        elif speed[1] < 0 and speed[1] < speed[0]:
            self.axis = 1
            self.dir = 0
        elif speed[1] > 0 and speed[1] > speed[0]:
            self.axis = 1
            self.dir = 1
        if self.axis == 0:
            self.bg_2_pos = [self.rect.width * (-1 if self.dir == 0 else 1), 0]
        else:
            self.bg_2_pos = [0, self.rect.height * (-1 if self.dir == 0 else 1)]

    def update(self, *args, **kwargs) -> None:
        # MOVE BOTH BACKGROUNDS AN EQUAL AMOUNT
        dt = self.game.delta_time
        self.bg_pos = [self.bg_pos[0] - (self.speed[0] * dt), self.bg_pos[1] - (self.speed[1] * dt)]
        self.bg_2_pos = [self.bg_2_pos[0] - (self.speed[0] * dt), self.bg_2_pos[1] - (self.speed[1] * dt)]
        # LOOP DETECTING 
        axis = self.rect.width if self.axis == 0 else self.rect.height
        # MOVE FIRST BACKGROUND IF IT GOES PASSED ITS AXIS EDGE
        if get_truth(self.bg_pos[self.axis], "<=" if self.dir == 1 else ">=", axis * (-1 if self.dir == 1 else 1)):
            self.bg_pos[self.axis] = axis * (1 if self.dir == 1 else -1)
        # MOVE SECOND BACKGROUND IF IT GOES PASSED ITS AXIS EDGE
        if get_truth(self.bg_2_pos[self.axis], "<=" if self.dir == 1 else ">=", axis * (-1 if self.dir == 1 else 1)):
            self.bg_2_pos[self.axis] = axis * (1 if self.dir == 1 else -1)
        self.layers[0]["pos"] = self.bg_pos
        self.layers[1]["pos"] = self.bg_2_pos