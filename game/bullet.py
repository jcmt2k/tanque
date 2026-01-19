import arcade
import math
from constants import *

class Bullet(arcade.Sprite):
    def __init__(self, image_name, scale, angle):
        super().__init__(f"{ASSET_PATH}{image_name}", scale)
        self.angle = angle
        self.change_x = math.sin(math.radians(self.angle)) * BULLET_SPEED
        self.change_y = math.cos(math.radians(self.angle)) * BULLET_SPEED
        self.lifetime = SCREEN_WIDTH / BULLET_SPEED  # Approximated lifetime
        self.collision_cooldown = 0

    def update(self, delta_time: float = 1/60):
        super().update()
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1
            
    def bounce(self, wall):
        """Calculates correct bounce depending on wall orientation."""
        # Simple bounding box collision response
        # If we hit left or right side of wall, reverse X
        if self.center_x < wall.left or self.center_x > wall.right:
             self.change_x *= -1
        # If we hit top or bottom, reverse Y
        elif self.center_y < wall.bottom or self.center_y > wall.top:
            self.change_y *= -1
        
        self.collision_cooldown = 5 # Prevent sticking
