import datetime
from typing import Any
from abc import ABCMeta, abstractmethod
import pygame as py
from json import load
from datetime import datetime as time

from engine.game_objects.modules import IModule


class IAnimationModule(IModule):
    __metaclass__ = ABCMeta

    def __init__(self, obj, use_obj_image: bool = True):
        self.animations = {}
        self.use_obj_image = use_obj_image
        self.should_animate = False
        self.active_anims = []
        self.reversed_anims = []
        self.current_frame = 0
        self.last_frame_change = 0
        super(IAnimationModule, self).__init__(obj)

    def set_animation_dict(self, animations: dict): self.animations = animations
    def add_animation_by_dict(self, name: str,  _dict: dict): self.animations[name] = _dict

    def add_animation_by_json(self, file: str):
        with open(f"{self.obj.game.gameDir}\\{file}", "r") as f:
            data = load(f)
            f.close()
        self.animations[data["name"]] = {
            "layer": data["layer"],
            "frames": [self.obj.sprite_sheet[x] for x in data["animation"]["frames"]],
            "frame_time": int(data["frame_time"]),
            "loop": True if data["animation"]["loop"] == "True" else False
        }

    def play(self, animation):
        if self.animations.keys().__contains__(animation):
            self.active_anims.append(animation)

    def stop(self, animation):
        self.active_anims.remove(animation)
        self.current_frame = 0

    def set_image(self, image, layer_id):
        pos = self.obj.get_layer_position(layer_id)
        self.obj.set_layer(image, pos, layer_id)

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        # SHOULD ANIMATE
        if self.should_animate:
            # IS ANIMATION SELECTED
            for active_anim in self.active_anims:

                if active_anim is not None:
                    anim = self.animations[active_anim]
                    # SET CURRENT FRAME IF NOT ALREADY
                    if self.current_frame <= len(anim["frames"])-1:
                        anim_frames = anim["frames"]
                        if self.obj.get_layer(anim["layer"]) != anim_frames[self.current_frame]:
                            self.set_image(anim_frames[self.current_frame], anim["layer"])
                    # CHECK TIME FOR FRAME CHANGE
                    if self.last_frame_change + anim["frame_time"] < int(time.now().timestamp() * 1000):
                        self.last_frame_change = int(time.now().timestamp() * 1000)
                        # IF LOOPING
                        if anim["loop"]:
                            self.current_frame = 0 if self.current_frame == len(anim["frames"])-1 else self.current_frame + 1
                        else:
                            # IF FRAMES LEFT
                            if self.current_frame == len(anim["frames"]) - 1:
                                try:
                                    anim['callback']()
                                except:
                                    pass
                                self.active_anims.remove(active_anim)
                                self.current_frame = 0
                            else:
                                self.current_frame += 1
