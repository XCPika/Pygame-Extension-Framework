from __future__ import annotations

# Color - Data structure for storing a color
class Color:
    def __init__(self, *args):
        self.RGBA = tuple(v*255 for v in args)
        self.RGB = tuple(v for v in self.RGBA if v > 3)
        self.r, self.g, self.b, self.a = self.RGBA[0], self.RGBA[1], self.RGBA[2], self.RGBA[3]

    @staticmethod
    def color_blend(c1: tuple | Color , c2: tuple | Color) -> Color:
        if isinstance(c1, tuple): c1 = Color(*c1)
        if isinstance(c2, tuple): c2 = Color(*c2)
        a = c1.a + (c2.a * (255 - c1.a) / 255)
        r = (c1.r * c1.a + c2.r * c2.a * (255 - c1.a) / 255) / a
        g = (c1.g * c1.a + c2.g * c2.a * (255 - c1.a) / 255) / a
        b = (c1.b * c1.a + c2.b * c2.a * (255 - c1.a) / 255) / a
        return Color(int(r), int(g), int(b), int(a))
