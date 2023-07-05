import pygame.math
from pygame.math import Vector2 as V2, Vector3 as V3


# Vector2 - Custom Vector2 based on a pygame.V2 for easier extension
class Vector2(V2):
    def __init__(self, x, y): super(Vector2, self).__init__(x, y)
    def __mul__(self, other): return Vector2(self.x * other.x, self.y * other.y)
    @staticmethod
    def get_diff(a: pygame.math.Vector2, b: pygame.math.Vector2): return Vector2(a.x, a.y).xy - Vector2(b.x, b.y).xy
    @staticmethod
    def get_diff_tuple(a: tuple, b: tuple): return Vector2(a[0], a[1]).xy - Vector2(b[0], b[1]).xy


# Vector3 - Custom Vector3 based on a pygame.V3 for easier extension
class Vector3(V3):
    def __init__(self, x, y, z): super(Vector3, self).__init__(x, y, z)
    @staticmethod
    def get_diff(a, b): return Vector3((a.x, a.y, a.z)).xyz - Vector3((b.x, b.y, b.z)).xyz
    @staticmethod
    def get_diff_tuple(a, b): return Vector3((a[0], a[1], a[2])).value - Vector3((b[0], b[1], b[2])).value
