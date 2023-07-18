# GameObject

## Contents
- Functions
  - \_\_init\_\_ ()

## Functions

**\_\_init\_\_**

 Signature: \_\_init\_\_(group: str = "all_sprites", game: engine.game_engine.Pygame = None)<br>
 Description: Runs the basic setup of the game object. If overridden run the super().\_\_init\_\_(group, game) function.<br>
 Usage: 
 ```python
class Player(GameObject):
    def __init__(group: str = "player", game: engine.game_engine.Pygame = None):
        super(Player, self).__init__(group, game)
   
Player(game=self)
```
