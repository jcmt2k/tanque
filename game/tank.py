import arcade
import math
from constants import *
from bullet import Bullet

class Tank(arcade.Sprite):
    def __init__(self, color, scale):
        self.my_color = color
        image_name = f"tank_{self.my_color}.png"
        super().__init__(f"{ASSET_PATH}{image_name}", scale)
        
        self.bullet_name = f"bullet_{self.my_color}.png"
        self.angle_speed = 0
        self.speed = 0
        self.fire_cooldown = 0
        self.bullet_offset = BULLET_OFFSET  # Distance from center to spawn bullet

    def update(self, delta_time: float = 1/60):
        # Rotate
        self.angle -= self.angle_speed
        
        # Calculate velocity vector
        # Reverting to standard math (Positive).
        # We will handle "Forward/Backward" mapping in the Input handling (main.py)
        # to ensure W moves in the visual direction of the cannon.
        self.change_x = math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed
        
        super().update()
        
        # Screen wrapping
        if self.left > SCREEN_WIDTH:
            self.right = 0
        elif self.right < 0:
            self.left = SCREEN_WIDTH
        if self.top > SCREEN_HEIGHT:
            self.bottom = 0
        elif self.bottom < 0:
            self.top = SCREEN_HEIGHT
            
        # Cooldown management
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

    def fire(self):
        """Attempts to fire a bullet. Returns Bullet instance or None."""
        if self.fire_cooldown == 0:
            # Fire from the "Back" (which appears to be the visual Front)
            #bullet_angle = self.angle + 180 
            bullet_angle = self.angle 
            bullet = Bullet(self.bullet_name, BULLET_SCALE, bullet_angle)
            
            # Spawn bullet at the cannon tip (inverted direction)
            # Increased offset to 60 to ensure it clears the tank body
            # offset vector based on new bullet angle
            offset = BULLET_OFFSET
            bullet.center_x = self.center_x + math.sin(math.radians(bullet_angle)) * offset
            bullet.center_y = self.center_y + math.cos(math.radians(bullet_angle)) * offset 
            self.fire_cooldown = FIRE_RATE
            return bullet
        return None
