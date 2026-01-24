import arcade
import random
from constants import *

class PowerUp(arcade.Sprite):
    def __init__(self, x, y):
        self.type = random.choice(list(POWERUP_CONFIG.keys()))
        
        config = POWERUP_CONFIG[self.type]
        
        # Determine color/visual based on type
        # Ideally we'd valid pngs, but for now we'll use simple colored circles via Arcade's make_circle_texture if possible,
        # or just load a dummy image and tint it.
        # Since we might not have assets, let's try to use standard shapes or existing assets tinted.
        
        filename = f"{ASSET_PATH}bullet.png" # Placeholder
        super().__init__(filename, POWERUP_SCALE)
        
        self.center_x = x
        self.center_y = y
        
        self.color = config["color"]
        # Texture name is less relevant if we just rely on color, but keeping it simple
        self.texture_name = config["name"].lower().replace(" ", "_")

    def draw(self, **kwargs):
        # Custom draw to make it look distinct if sprites are simple
        super().draw(**kwargs)
        # Draw a ring to indicate it's special
        arcade.draw_circle_outline(self.center_x, self.center_y, 15, self.color, 2)
