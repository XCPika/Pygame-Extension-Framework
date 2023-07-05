import pygame as py


class ImageEdit:
    @staticmethod
    def fill(image: py.surface.Surface, color) -> py.surface.Surface:
        w, h = image.get_size()
        for x in range(w):
            for y in range(h):
                image.set_at((x, y),
                             ImageEdit.colorBlend(color,
                                                  image.get_at((x, y))
                                                  )
                             )
        return image
