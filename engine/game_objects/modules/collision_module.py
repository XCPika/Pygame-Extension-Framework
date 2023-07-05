from typing import Any
from abc import ABCMeta, abstractmethod

from pygame import sprite

from engine.game_objects.modules import IModule


class ICollisionModule(IModule):
    __metaclass__ = ABCMeta

    def __init__(self, obj, mask=False, callback=None):
        self.masked = mask
        self.collision_groups = ["all_sprites"]
        self.callback = callback
        super(ICollisionModule, self).__init__(obj)

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None: self.run_collision_check()

    @staticmethod
    def masked_collision_callback(a, b) -> bool: return False

    def run_collision_check(self):
        if self.tick:
            for group in self.collision_groups:
                hits = sprite.spritecollide(self.obj,
                                            self.obj.game.groups[group],
                                            False,
                                            collided=self.masked_collision_callback if self.masked else None)
                self._loop_hits(hits, group)

    def _loop_hits(self, hits, group):
        if hits:
            if hits.__contains__(self):
                hits.remove(self)
            if hits:
                if hits[0].has_module("collision"):
                    if hits[0].get_module("collision").tick:
                        self.callback(hits[0], group)
                else:
                    hits.pop(0)
                    self._loop_hits(hits, group)
