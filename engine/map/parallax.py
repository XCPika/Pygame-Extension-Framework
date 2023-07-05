from typing import Any
import pygame as py

from engine.game_objects.game_object import IGameObject


class Parallax(IGameObject):
    def __init__(self, game, data: dict, follow_target: str = None):
        super(Parallax, self).__init__("map", game)
        self.follow_target = follow_target
        self.layers = [py.image.load(f"{self.game.game_dir}\\data\\images\\{x}").convert_alpha() for x in data["layers"]]
        self.surface_size = data["size"]
        self.scroll_axis = data["scroll_axis"]
        self.scroll_speed = data["scroll_speed"]
        self.pos = (0, 0)
        self.image = self.create_layers()
        self.rect = self.image.get_rect()

    def set_follow_target(self, target: str): self.follow_target = target
    def calculate_offset(self) -> tuple: return 0, 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image = self.create_layers()
        self.rect = self.image.get_rect()

    def create_layers(self) -> py.Surface:
        surface = py.Surface(self.surface_size)
        init_x, init_y = self.pos[0], self.pos[1]
        offset = (0, 0)
        for i, v in enumerate(self.layers):
            x, y, i = init_x, init_y, len(self.layers) - i
            if self.follow_target is not None:
                offset = self.calculate_offset()
                if offset[0] != 0:
                    x = self.pos[0] - ((offset[0] * self.scroll_speed) * i)
                    print(x)
            surface.blit(v, (x, y))
        self.pos = (init_x - offset[0], 0)
        return surface
