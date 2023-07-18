import pygame as py

from engine.errors.invalid_argument_exception import InvalidArgumentException
from engine.color import Color


class DebugHandler:
    def __init__(self, debug: bool = False, game: 'engine.game_engine.Pygame' = None):
        if game is None:
            raise InvalidArgumentException()
        self._debug = debug
        self.game = game
    
    def set_debug(self, debug: bool): self._debug = debug

    def __repr__(self) -> str: return str(self.debug)
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, bool):
            raise TypeError
        return self._debug == __value

    def debug_collision(self, sprite: 'engine.game_objects.IGameObject'):
        if self._debug:
            if sprite.debug:
                self.display_masked_collisions(sprite)
                self.display_rect_collisions(sprite)

    def display_rect_collisions(self, sprite: 'engine.game_objects.IGameObject'): 
        py.draw.rect(
            py.display.get_surface(),
            Color(1, 0, 0, 1).RGBA, sprite.rect, 1
        )

    def display_masked_collisions(self, sprite: 'engine.game_objects.IGameObject'):
        if hasattr(sprite, "mask"):
            if sprite.mask is not None:
                self.game.screen.blit(sprite.mask.to_surface(), sprite.rect)

