from abc import ABCMeta, abstractmethod
from typing import Any

import pygame as py


# Module - Used to create custom modules for GameObjects
class Module:
    def __init__(self, obj, tick=True):
        self.obj = obj
        self.tick = tick
    # Update -> Runs during the game update for the object if self.tick is True
    def update(self, *args: Any, **kwargs: Any) -> None: pass


class IModule(Module):
    __metaclass__ = ABCMeta
    @abstractmethod
    def __init__(self, obj, tick=True): super(IModule, self).__init__(obj, tick)
    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None: super(IModule, self).update(args, kwargs)
    

