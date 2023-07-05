from typing import Any
from abc import ABCMeta, abstractmethod
from collections import UserDict

import pygame as py
from engine.game_objects.modules.module import IModule


# Module Handler #
class ModuleHandler(UserDict):
    def __setitem__(self, key, obj): super().__setitem__(key, obj)
    def get_module(self, key: str): return self[key]
    def set_module(self, key: str, module: IModule): self[key] = module
    def update(self): [self[x].update() for x in self if self[x].tick]
    def contains_key(self, obj) -> bool: return self.keys().__contains__(obj)


# Game Object #
class GameObject(py.sprite.Sprite):
    def __init__(self, group="all_sprites", game=None):
        self.group = game.groups[group]
        self.game = game
        self.image, self.rect = "", (0, 0)
        self.object_key = None
        self.debug = True
        self.modules = ModuleHandler()
        py.sprite.Sprite.__init__(self, game.groups[group])

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.modules.update()
        super(GameObject, self).update(args, kwargs)

    def set_object_key(self, key: str): self.object_key = key
    def destroy(self): self.game.objects.pop(self.object_key)
    def has_module(self, cls: str) -> bool: return self.modules.contains_key(cls)
    def get_module(self, cls: str) -> object: return self.modules.get_module(cls)
    def set_module(self, key: str, module: IModule): self.modules.set_module(key, module)


# IGame Object - Interface for the Game Object class
class IGameObject(GameObject):
    __metaclass__ = ABCMeta
    # Constructor -> Override, always run Super().__init__()
    @abstractmethod
    def __init__(self, group="all_sprites", game=None): super(IGameObject, self).__init__(group, game)
    # Destroy -> Kills the game object
    def destroy(self): super(IGameObject, self).destroy()
    # Set Object Key -> Internally used by Object Handler
    def set_object_key(self, key): super(IGameObject, self).set_object_key(key)
    def has_module(self, cls: str) -> bool: return super(IGameObject, self).has_module(cls)
    def get_module(self, cls: str) -> object: return super(IGameObject, self).get_module(cls)
    def set_module(self, key: str, module: IModule): super(IGameObject, self).set_module(key, module)
