import arcade
import random
from constants import SCREEN_HEIGHT

class AcidDrop(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.change_y = -random.uniform(3, 7) # Fall speed
        
        # Simple visual: Small green rectangle or line
        self.texture = arcade.make_soft_square_texture(4, arcade.color.LIME, outer_alpha=255)
        self.scale = 1.0

    def update(self, delta_time: float = 1/60):
        self.center_y += self.change_y
        
        # Kill if off screen
        if self.top < 0:
            self.remove_from_sprite_lists()
