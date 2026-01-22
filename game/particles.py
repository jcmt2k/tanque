import arcade
import random
import math

class Particle(arcade.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.color = color
        
        # Random velocity
        speed = random.uniform(2, 5)
        angle = random.uniform(0, 360)
        self.change_x = math.sin(math.radians(angle)) * speed
        self.change_y = math.cos(math.radians(angle)) * speed
        
        # Simple square texture (created programmatically)
        self.texture = arcade.make_soft_square_texture(10, self.color, outer_alpha=255)
        
        self.scale = random.uniform(0.5, 1.0)
        self.alpha = 255
        self.fade_rate = random.randint(5, 15)

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.alpha -= self.fade_rate
        if self.alpha <= 0:
            self.remove_from_sprite_lists()
        else:
            self.alpha = max(0, self.alpha)
