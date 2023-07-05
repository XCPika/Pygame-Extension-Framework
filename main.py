import pygame as py
from engine.game_engine import Pygame
from engine.color import Color

# MINIMAL RUNNING EXAMPLE #
# Main Game Engine Object #
class Game(Pygame):
    def __init__(self):
        super(Game, self).__init__(1280, 720, "Space Game", fps_target=60)
        self.groups["player"] = py.sprite.Group()
        self.load_data()
        self.loop()

    def load_data(self):
        super(Game, self).load_data() # Required to set the base dir of the game for easy access in objects without recalculating where to split the path (self.game_dir)

    def draw(self):
        self.screen.fill(Color(1, 1, 1, 1).RGB) # self.screen.fill((255, 255, 255)). Color class is used mostly for storing colors to easily recall but may get more features later
        super(Game, self).draw() # Required to call the draw function for registered objects
        # UNCOMMENT FOR RECT DEBUGGING
        # for group in self.groups.keys():
        #     for sprite in self.groups[group]:
        #         if self.debug:
        #             if sprite.debug:
        #                 py.draw.rect(py.display.get_surface(), Color(1, 0, 0, 1).RGBA, sprite.rect, 1)
        super(Game, self).render_display() # Required to call the render update of the display (py.display.flip())

    def update(self):
        super(Game, self).update()
        for event in py.event.get():
            # COMMENT TO REMOVE MANUAL WINDOW RESIZING SUPPORT
            if event.type == py.VIDEORESIZE:
                self.windowSize = (event.w, event.h)
                py.display._resize_event(event)
            if event.type == py.QUIT:
                self.quit()
            if event.type == py.KEYDOWN:
                # UNCOMMENT TO TOGGLE DEBUGGING
                # if event.key == py.K_c:
                #     self.debug = not self.debug
                if event.key == py.K_ESCAPE:
                    self.quit()

    def loop(self):
        while self.RUNNING:
            self.update()
            self.draw()


g = Game()
