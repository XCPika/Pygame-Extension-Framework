import pygame as py
from engine.game_engine import Pygame
from engine.color import Color
from engine.map import LoopingMap


# MINIMAL RUNNING EXAMPLE #
# Main Game Engine Object #
class Game(Pygame):
    def __init__(self):
        super(Game, self).__init__(1280, 720, "Space Game", fps_target=60)
        self.add_group("map") # The order groups are registered in is what pygame uses as layer render order. First added is first rendered (Put things like map groups in first)
        # SETUP GAME AXIS CONTROLS (IControlModule().get_axis("move_left"))
        self.axis = {'move_left': {py.K_a: -1, py.K_d: 1}, 'move_up': {py.K_w: -1, py.K_s: 1}}
        self.load_data()
        self.start_game_loop()

    def load_data(self):
        super(Game, self).load_data() # Required to set the base dir of the game for easy access in objects without recalculating where to split the path (self.game_dir)
        self.objects['map'] = LoopingMap(self, "data/images/background.png", [2, 0]) # Looping map uses the images size to calculate its looping. You may need to rescale your image to fit your game area (Window scaling will handle it after as long as it covers the initial screen). Supports vertical or horizontal but not both (Hopefully in future revisions)


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


if __name__ == '__main__':
    g = Game()
