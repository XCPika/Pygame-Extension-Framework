import pygame as py
from engine.game_engine import Pygame
from engine.color import Color
from engine.game_objects import IGameObject
from engine.game_objects.modules import IControlModule, IAnimationModule
from engine.image import SpriteSheet


# Player Object #
class Player(IGameObject):
    def __init__(self, pos: tuple, game: Pygame):
        super(Player, self).__init__('player', game)
        self.modules.set_module("control", IControlModule(self, callback=self.callback_input_tick)) # or self.modules['control'] = IControlModule(self, callback=self.callback_input_tick) 
        self.modules.set_module("animation", IAnimationModule(self))

        self.pos = pos 
        self.last_pos = (0, 0) # Used as part of animation logic (Not required)

        self.sprite_sheet = SpriteSheet(f"{self.game.game_dir}/data/images/ship_00.png", 66, 38).get_image_array()
        self.add_layer(self.sprite_sheet[0], self.pos)
        self.rect = self.get_layer_image(0).get_rect(center=self.pos)
        # Optionally: self.modules.get_module("animation").add_animation_by_json(file_location: str) file_location is relative to game_dir
        self.modules.get_module("animation").add_animation_by_dict("engines_on",
            {
                "layer": 0,
                "frames": [self.sprite_sheet[1]],
                "frame_time": 500,
                "loop": False,
                "callback": self.callback_engine_anim_ended
            }
        )
        self.modules["animation"].should_animate = True
        self.rect = self.get_layer_image(0).get_rect(center=self.pos)
    
    def callback_engine_anim_ended(self):
        self.set_layer(self.sprite_sheet[0], layer_id=0)

    def callback_input_tick(self):
        self.last_pos = self.pos
        self.pos = self.modules["control"].get_mouse_pos()

    def update(self):
        if self.last_pos != self.pos:
            self.modules["animation"].play("engines_on")
                
        self.rect = self.get_layer_image(0).get_rect(center=self.pos)
        super(Player, self).update()


# ANIMATION EXAMPLE #
# Main Game Engine Object #
class Game(Pygame):
    def __init__(self):
        super(Game, self).__init__(1280, 720, "Space Game", fps_target=60)
        self.add_group("player") # The order groups are registered in is what pygame uses as layer render order. First added is first rendered (Put things like map groups in first)
        self.load_data()
        self.start_game_loop()

    def load_data(self):
        super(Game, self).load_data() # Required to set the base dir of the game for easy access in objects without recalculating where to split the path (self.game_dir)
        self.objects["player"] = Player((self.screen.get_width() / 2, self.screen.get_height() / 2), self) # Adds a GameObject to the ObjectHandler so that update and draw calls are triggered correctly


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
