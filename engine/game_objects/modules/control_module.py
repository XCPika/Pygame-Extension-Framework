from typing import Any
from abc import ABCMeta, abstractmethod
import pygame as py

from engine.game_objects.modules import IModule


class IControlModule(IModule):
    __metaclass__ = ABCMeta

    def __init__(self, obj, mask=False, callback=None):
        self.callback = callback
        super(IControlModule, self).__init__(obj)

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None: self.callback()

    # GetAxis - axis: str -> Checks the py.key.get_pressed() to see if the axis sent through was pressed and returns its
    #                        Corresponding value
    def get_axis(self, axis) -> int:
        keys = py.key.get_pressed()
        for key in self.obj.game.axis[axis]:
            if keys[key]:
                return self.obj.game.axis[axis][key]
        return 0

    # STATIC METHODS
    @staticmethod
    def get_key(kbd_key) -> bool: return py.key.get_pressed()[kbd_key]
    @staticmethod
    def get_mouse_pos() -> tuple: return py.mouse.get_pos()
    @staticmethod
    def get_mouse_click() -> bool: return py.mouse.get_pressed(3)
