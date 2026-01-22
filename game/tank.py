import arcade
import math
from constants import *
from bullet import Bullet

class Tank(arcade.Sprite):
    def __init__(self, color, scale):
        self.my_color = color
        self.hp = TANK_STARTING_HP
        self.max_hp = TANK_STARTING_HP
        image_name = f"tank_{self.my_color}.png"
        super().__init__(f"{ASSET_PATH}{image_name}", scale)
        
        self.bullet_name = f"bullet_{self.my_color}.png"
        self.angle_speed = 0
        self.speed = 0
        self.fire_cooldown = 0
        
        # Ammo
        self.ammo = MAX_AMMO
        self.max_ammo = MAX_AMMO
        self.is_reloading = False
        self.reload_timer = 0
        
        self.text_reloading = arcade.Text(
            "RECARGANDO...",
            0, 0, # Position updated in draw
            arcade.color.WHITE,
            font_size=10,
            anchor_x="center"
        )
        
        self.bullet_offset = BULLET_OFFSET  # Distance from center to spawn bullet

        # Power-ups
        self.is_shielded = False
        self.shield_timer = 0
        self.speed_boost_timer = 0
        self.triple_shot_timer = 0
        self.base_speed = TANK_SPEED # Store constant
        self.current_max_speed = TANK_SPEED

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
            
        # Reload management
        if self.is_reloading:
            self.reload_timer -= delta_time
            if self.reload_timer <= 0:
                self.ammo = self.max_ammo
                self.is_reloading = False
                self.reload_timer = 0

        # Power-up Timers
        if self.is_shielded:
            self.shield_timer -= delta_time
            if self.shield_timer <= 0:
                self.is_shielded = False
        
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= delta_time
            if self.speed_boost_timer <= 0:
                self.current_max_speed = self.base_speed
        
        if self.triple_shot_timer > 0:
            self.triple_shot_timer -= delta_time

    def apply_powerup(self, p_type):
        """Applies a powerup effect."""
        if p_type == POWERUP_TYPE_SHIELD:
            self.is_shielded = True
            self.shield_timer = POWERUP_DURATION
        elif p_type == POWERUP_TYPE_SPEED:
            self.speed_boost_timer = POWERUP_DURATION
            self.current_max_speed = self.base_speed * 1.5
        elif p_type == POWERUP_TYPE_TRIPLE:
            self.triple_shot_timer = POWERUP_DURATION

    def fire(self):
        """Attempts to fire a bullet. Returns Bullet instance or None."""
        if self.fire_cooldown == 0 and not self.is_reloading and self.ammo > 0:
            self.ammo -= 1
            if self.ammo <= 0:
                self.is_reloading = True
                self.reload_timer = RELOAD_TIME
                
            # Fire from the "Back" (which appears to be the visual Front)
            #bullet_angle = self.angle + 180 
            base_angle = self.angle 
            
            bullets_to_spawn = []
            
            angles = [base_angle]
            if self.triple_shot_timer > 0:
                angles = [base_angle - 15, base_angle, base_angle + 15]
            
            for ang in angles:
                bullet = Bullet(self.bullet_name, BULLET_SCALE, ang)
                offset = self.bullet_offset # Use instance var
                bullet.center_x = self.center_x + math.sin(math.radians(ang)) * offset
                bullet.center_y = self.center_y + math.cos(math.radians(ang)) * offset 
                bullets_to_spawn.append(bullet)

            self.fire_cooldown = FIRE_RATE
            return bullets_to_spawn
        return []
        return None
        
    def draw_health_bar(self):
        """Draws a simple health bar above the tank."""
        if self.hp < self.max_hp:
            # Draw background (Red)
            # Using lrbt per modern Arcade requirements (Left, Right, Bottom, Top)
            arcade.draw_lrbt_rectangle_filled(
                self.center_x - HEALTH_BAR_WIDTH / 2,
                self.center_x + HEALTH_BAR_WIDTH / 2,
                self.center_y + 40 - HEALTH_BAR_HEIGHT / 2, # Bottom
                self.center_y + 40 + HEALTH_BAR_HEIGHT / 2, # Top
                arcade.color.RED
            )
            
            # Draw current health (Green)
            health_width = HEALTH_BAR_WIDTH * (self.hp / self.max_hp)
            # Calculate left position based on centered bar
            bar_left = self.center_x - HEALTH_BAR_WIDTH / 2
            
            arcade.draw_lrbt_rectangle_filled(
                bar_left,
                bar_left + health_width,
                self.center_y + 40 - HEALTH_BAR_HEIGHT / 2, # Bottom
                self.center_y + 40 + HEALTH_BAR_HEIGHT / 2, # Top
                arcade.color.GREEN
            )
            
        if self.is_shielded:
             arcade.draw_circle_outline(self.center_x, self.center_y, 30, arcade.color.CYAN, 2)
            
        # Draw Ammo (Yellow dots below health)
        start_x = self.center_x - 20
        for i in range(self.max_ammo):
            color = arcade.color.YELLOW if i < self.ammo else arcade.color.GRAY
            arcade.draw_circle_filled(
                start_x + i * 10,
                self.center_y + 30,
                3,
                color
            )
        
        # Draw Reloading Text
        if self.is_reloading:
            self.text_reloading.x = self.center_x
            self.text_reloading.y = self.center_y + 50
            self.text_reloading.draw()
