from __future__ import annotations
from typing import Any
from abc import ABCMeta, abstractmethod
from collections import UserDict

import pygame as py
from engine.game_engine import Pygame
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
    def __init__(self, group="all_sprites", game: Pygame=None):
        self.group = game.groups[group]
        self.draw_sprite = False if group == "handler" else True
        self.game = game
        self.layers = []
        self.primary_layer = None
        self.rect = "", (0, 0)
        self.object_key = None
        self.debug = False if group == "handler" else True
        self.modules = ModuleHandler()
        py.sprite.Sprite.__init__(self, game.groups[group])

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.modules.update()
        super(GameObject, self).update(args, kwargs)

    def draw(self):
        size = self.get_layer_image(self.primary_layer if self.primary_layer is not None else 0).get_size() 
        surface = py.Surface(size, flags=py.SRCALPHA)
        for spr in self.layers:
            surface.blit(spr["image"], spr["pos"])
        return surface, self.rect.topleft
    
    def destroy(self): 
        del self.game.objects[self.object_key]

    def set_object_key(self, key: str): self.object_key = key
    def has_module(self, cls: str) -> bool: return self.modules.contains_key(cls)
    def get_module(self, cls: str) -> object: return self.modules.get_module(cls)
    def set_module(self, key: str, module: IModule): self.modules.set_module(key, module)
    def has_layer(self, layer_id: int = 0) -> bool: return len(self.layers) == layer_id + 1
    def get_layer(self, layer_id: int = 0) -> dict[py.Surface, tuple]: return self.layers[layer_id]
    def get_layer_image(self, layer_id: int = 0) -> py.Surface: return self.get_layer(layer_id)["image"]
    def get_layer_position(self, layer_id: int = 0) -> py.Surface: return self.get_layer(layer_id)["pos"]
    def add_layer(self, image: str | py.Surface, pos: tuple = (0, 0), primary: bool = False): 
        self.layers.append(
            {
                "image": image if not isinstance(image, str) else py.image.load(image).convert_alpha(),
                "pos": pos
            }
        )
        if (self.primary_layer is None) | primary: self.primary_layer = len(self.layers) - 1
    def set_layer(self, image: str | py.Surface, pos: tuple = (0, 0), layer_id: int = 0):
        self.layers[layer_id] = {
            "image": image if not isinstance(image, str) else py.image.load(image).convert_alpha(),
            "pos": pos
        }
        


# IGame Object - Interface for the Game Object class
class IGameObject(GameObject):
    __metaclass__ = ABCMeta
    # Constructor -> Override, always run Super().__init__()
    @abstractmethod
    def __init__(self, group: str = "all_sprites", game: Pygame = None): super(IGameObject, self).__init__(group, game)
    # Destroy -> Kills the game object
    def destroy(self): super(IGameObject, self).destroy()
    # Set Object Key -> Internally used by Object Handler
    def set_object_key(self, key: str): super(IGameObject, self).set_object_key(key)
    # Set Module -> Used to add IModules to the GameObject
    def set_module(self, key: str, module: IModule): super(IGameObject, self).set_module(key, module)
    # Has Module -> Check if the GameObject has an IModule registered with that key
    def has_module(self, cls: str) -> bool: return super(IGameObject, self).has_module(cls)
    def get_module(self, cls: str) -> object: return super(IGameObject, self).get_module(cls)
    def set_layer(self, image: str | py.Surface, pos: tuple = (0, 0), layer_id: int = 0): super(IGameObject, self).set_layer(image, pos, layer_id)
    def add_layer(self, image: str | py.Surface, pos: tuple = (0, 0), primary: bool = False): super(IGameObject, self).add_layer(image, pos, primary)
    def has_layer(self, layer_id: int = 0) -> bool: return super(IGameObject, self).has_layer(layer_id)
    def get_layer(self, layer_id: int = 0) -> py.Surface: return super(IGameObject, self).get_layer(layer_id)
    def get_layer_image(self, layer_id: int = 0) -> py.Surface: return super(IGameObject, self).get_layer_image(layer_id)
    def get_layer_position(self, layer_id: int = 0) -> py.Surface: return super(IGameObject, self).get_layer_position(layer_id)
    
