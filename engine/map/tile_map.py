import pygame as py
import pytmx
import math

from engine.game_objects.game_object import GameObject
from engine.math.vector import Vector2


class NoMapFolderRegisteredException(Exception):
    ...


class TileMapCamera:
    def __init__(self, game, size, follow_target: str = None):
        self.size = Vector2(size.x, size.y)
        self.camera = py.Rect(0, 0, self.size.x, self.size.y)
        self.game = game
        self.follow_target = follow_target

    def apply(self, entity):
        try:
            return entity.rect.move(self.camera.topleft)
        except:
            pass

    def apply_rect(self): return self.game.objects["map"].rect.move(self.camera.topleft)

    def update(self):
        if self.follow_target is not None:
            target = self.game.objects[self.follow_target]
            x = -target.rect.centerx + self.game.screen.get_rect().centerx
            y = -target.rect.centery + self.game.screen.get_rect().centery
            x = min(0, x)
            y = min(0, y)
            x = max(x, -(self.game.objects["map"].full_size.x - self.game.screen.get_rect().width))
            y = max(y, -(self.game.objects["map"].full_size.y - self.game.screen.get_rect().height))
            self.camera = py.Rect(x, y, *self.size.xy)


class TileMap(GameObject):
    def __init__(self, game, file: str, follow_camera: bool = True, follow_target=None):
        super(TileMap, self).__init__("map", game)
        self.game, self.file = game, file
        self.follow_camera = follow_camera
        self.follow_target = follow_target
        self.camera = None
        if self.game.map_dir is None:
            raise NoMapFolderRegisteredException()
        self.draw_map()
        if self.follow_camera:
            self.camera = TileMapCamera(game, self.map_size, self.follow_target)

    def update(self):
        if self.follow_camera:
            self.camera.update()

    def draw_map(self):
        self.map_data = pytmx.load_pygame(f"{self.game.map_dir}\\{self.file}", pixelalpha=True)
        self.map_size = Vector2(self.map_data.width, self.map_data.height)
        self.tile_size = Vector2(self.map_data.tilewidth, self.map_data.tileheight)
        self.full_size = Vector2(self.map_size.x * self.tile_size.x,
                                 self.map_size.y * self.tile_size.y)
        self.image = self.render()
        self.rect = self.image.get_rect()
        self.draw_map_objects()

    def draw_map_objects(self):
        for tile_obj in self.map_data.objects:
            # .x .y .width .height .name
            pass

    def render(self) -> py.Surface:
        surface = py.Surface(self.map_size * self.tile_size)
        get_tile_image = self.map_data.get_tile_image_by_gid
        for layer in self.map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gID in layer:
                    tile = get_tile_image(gID)
                    if tile:
                        surface.blit(tile, ((x * self.tile_size.x), (y * self.tile_size.y)))
        return surface
