import arcade
import random
from constants import *

class PowerUp(arcade.Sprite):
    def __init__(self, x, y):
        self.type = random.choice([POWERUP_TYPE_SHIELD, POWERUP_TYPE_SPEED, POWERUP_TYPE_TRIPLE, POWERUP_TYPE_ACID])
        
        # Determine color/visual based on type
        # Ideally we'd valid pngs, but for now we'll use simple colored circles via Arcade's make_circle_texture if possible,
        # or just load a dummy image and tint it.
        # Since we might not have assets, let's try to use standard shapes or existing assets tinted.
        
        filename = f"{ASSET_PATH}bullet.png" # Placeholder
        super().__init__(filename, POWERUP_SCALE)
        
        self.center_x = x
        self.center_y = y
        
        if self.type == POWERUP_TYPE_SHIELD:
            self.color = arcade.color.BLUE
            self.texture_name = "shield"
        elif self.type == POWERUP_TYPE_SPEED:
            self.color = arcade.color.YELLOW
            self.texture_name = "speed"
        elif self.type == POWERUP_TYPE_TRIPLE:
            self.color = arcade.color.RED
            self.texture_name = "triple"
        elif self.type == POWERUP_TYPE_ACID:
            self.color = arcade.color.LIME
            self.texture_name = "acid"
            
    def draw(self, **kwargs):
        # Custom draw to make it look distinct if sprites are simple
        super().draw(**kwargs)
        # Draw a ring to indicate it's special
        arcade.draw_circle_outline(self.center_x, self.center_y, 15, self.color, 2)
