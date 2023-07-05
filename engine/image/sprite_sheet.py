import pygame
from engine.math.vector import Vector2
from engine.errors.invalid_argument_exception import InvalidArgumentException


class SpriteSheet(object):
    def __init__(self, file_name: str, width: int = None, height: int = None):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
        if width is None:
            raise InvalidArgumentException()
        if height is None:
            raise InvalidArgumentException()
        self.sprite_size = Vector2(width, height)
        self.sheet_size = Vector2(self.sprite_sheet.get_width(), self.sprite_sheet.get_height())

    def get_image(self, x: int = 0, y: int = 0):
        image = pygame.Surface(self.sprite_size.xy, pygame.SRCALPHA, 32)
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.sprite_size.x, self.sprite_size.y))
        return image

    def get_image_array(self):
        image_array = []
        for iY in range(int(self.sheet_size.y / self.sprite_size.y)):
            for iX in range(int(self.sheet_size.x / self.sprite_size.x)):
                image_array.append(
                    self.get_image(iX * self.sprite_size.x, iY * self.sprite_size.y)
                )
        return image_array

