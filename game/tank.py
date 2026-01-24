import arcade
import math
from constants import *
from bullet import Bullet

import time

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
        
        self.text_health_warning = arcade.Text(
            "PELIGRO!",
            0, 0,
            arcade.color.RED,
            font_size=12,
            anchor_x="center",
            bold=True
        )
        
        self.bullet_offset = BULLET_OFFSET  # Distance from center to spawn bullet

        # Power-ups
        self.is_shielded = False
        self.shield_timer = 0
        self.rapid_fire_timer = 0
        self.triple_shot_timer = 0
        self.base_speed = TANK_SPEED 
        
    def update(self, delta_time: float = 1/60):
        # Rotate
        self.angle -= self.angle_speed
        
        # Calculate velocity vector
        self.change_x = math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed
        
        super().update()
        
        # Screen wrapping
        if self.left > GAME_RIGHT_X:
            self.right = GAME_LEFT_X
        elif self.right < GAME_LEFT_X:
            self.left = GAME_RIGHT_X
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
        
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= delta_time
        
        if self.triple_shot_timer > 0:
            self.triple_shot_timer -= delta_time

    def apply_powerup(self, p_type):
        """Applies a powerup effect."""
        config = POWERUP_CONFIG.get(p_type)
        if not config:
            return

        duration = config.get("duration", 10.0)

        if p_type == POWERUP_TYPE_SHIELD:
            self.is_shielded = True
            self.shield_timer = duration
        elif p_type == POWERUP_TYPE_RAPID_FIRE:
            self.rapid_fire_timer = duration
            # Refill ammo immediately on pickup? logical for "full bullets"
            self.ammo = self.max_ammo 
            self.is_reloading = False
        elif p_type == POWERUP_TYPE_TRIPLE:
            self.triple_shot_timer = duration

    def fire(self):
        """Attempts to fire a bullet. Returns Bullet instance or None."""
        # Determine current fire rate and ammo usage
        current_fire_rate = FIRE_RATE
        infinite_ammo = False
        
        if self.rapid_fire_timer > 0:
            current_fire_rate = POWERUP_CONFIG[POWERUP_TYPE_RAPID_FIRE]["fire_rate_cooldown"]
            infinite_ammo = POWERUP_CONFIG[POWERUP_TYPE_RAPID_FIRE]["infinite_ammo"]

        if self.fire_cooldown == 0 and not self.is_reloading and (self.ammo > 0 or infinite_ammo):
            if not infinite_ammo:
                self.ammo -= 1
                if self.ammo <= 0:
                    self.is_reloading = True
                    self.reload_timer = RELOAD_TIME
                
            base_angle = self.angle 
            
            bullets_to_spawn = []
            
            angles = [base_angle]
            if self.triple_shot_timer > 0:
                # Use spread from config if possible, else default 15
                spread = POWERUP_CONFIG[POWERUP_TYPE_TRIPLE]["spread_angle"]
                angles = [base_angle - spread, base_angle, base_angle + spread]
            
            for ang in angles:
                bullet = Bullet(self.bullet_name, BULLET_SCALE, ang)
                offset = self.bullet_offset # Use instance var
                bullet.center_x = self.center_x + math.sin(math.radians(ang)) * offset
                bullet.center_y = self.center_y + math.cos(math.radians(ang)) * offset 
                bullets_to_spawn.append(bullet)

            self.fire_cooldown = current_fire_rate
            return bullets_to_spawn
        return []
        
    def draw_indicators(self):
        """Draws indicators (Shield, Ammo) on/near the tank."""
        # Shield
        if self.is_shielded:
             arcade.draw_circle_outline(self.center_x, self.center_y, 30, arcade.color.BLUE, 2)
            
        # Low Health Warning
        if self.hp <= 1:
             # Flash effect based on time or random for simplicity without adding new timer
             if (int(time.time() * 4) % 2) == 0:
                 self.text_health_warning.x = self.center_x
                 self.text_health_warning.y = self.center_y + 40
                 self.text_health_warning.draw()
                 
                 arcade.draw_circle_outline(self.center_x, self.center_y, 25, arcade.color.RED, 2)

        # Discrete Ammo (Small dots below tank)
        start_x = self.center_x - 15
        
        display_ammo = self.ammo
        if self.rapid_fire_timer > 0:
            display_ammo = self.max_ammo
            
        for i in range(self.max_ammo):
            # Only draw available ammo or empty slots subtly
            if i < display_ammo:
                color = arcade.color.YELLOW
                if self.rapid_fire_timer > 0:
                     color = arcade.color.GOLD
                
                arcade.draw_circle_filled(
                    start_x + i * 8,
                    self.center_y - 30, # Below tank
                    3,
                    color
                )
            else:
                # Optionally draw empty dots very faintly
                arcade.draw_circle_filled(
                    start_x + i * 8,
                    self.center_y - 30,
                    2,
                    (50, 50, 50, 100) # Semi-transparent gray
                )
             
        
        if self.is_reloading:
            self.text_reloading.x = self.center_x
            self.text_reloading.y = self.center_y + 50
            self.text_reloading.draw()

    def update_ai(self, target, walls, delta_time):
        """Simple AI to control the tank."""
        if not target:
            self.speed = 0
            self.angle_speed = 0
            return []

        # 1. Targeting
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        target_angle = math.degrees(math.atan2(dx, dy)) # Note: atan2(x, y) for 0=North
        # Arcade angle 0 is East? No, Tank sprite usually 0 is Up/North if drawn that way.
        # Let's assume standard math: 0 is East. atan2(y, x).
        # But Sprite angle: 0 is right (East).
        # MyGame setup: P2 angle=180 (facing Left?).
        # Let's check atan2 usage. math.atan2(y, x).
        target_angle = math.degrees(math.atan2(dy, dx)) - 90 # Adjust for Sprite 0=North convention?
        # Actually, let's debug. Standard Tank sprites usually face UP (North) at angle 0.
        # So atan2(dy, dx) gives angle from East (0).
        # We need angle from North (0 is North? No, usually 0 is East in Arcade unless specified).
        # Let's assume 0 is East (Right). 
        # Then target_angle = degrees(atan2(dy, dx)).
        
        # Correction: arcade.Sprite 0 degrees is usually pointing RIGHT.
        # If tank image points UP, we need -90.
        # Let's assume standard behavior: angle is CCW from Right.
        target_angle = math.degrees(math.atan2(dy, dx)) - 90 # Assuming tank art faces Up.
        
        # Calculate difference
        diff = target_angle - self.angle
        # Normalize diff to -180 to 180
        while diff > 180: diff -= 360
        while diff < -180: diff += 360
        
        # Turn towards target
        if abs(diff) > 5:
            if diff > 0:
                self.angle_speed = TANK_TURN_SPEED
            else:
                self.angle_speed = -TANK_TURN_SPEED
        else:
            self.angle_speed = 0
            
        # 2. Movement (Maintain distance)
        desired_dist = 300
        if dist > desired_dist:
            self.speed = TANK_SPEED
        elif dist < desired_dist - 50:
            self.speed = -TANK_SPEED
        else:
            self.speed = 0
            
        # 3. Wall Avoidance (Very basic)
        # If we hit a wall recently (speed was 0 but we wanted to move?), logic is handled in main.py collision.
        # Here we just react to recoil?
        # Let's add simple random strafe if stuck?
        # For now, just focus on shooting.
        
        # 4. Shooting
        bullets = []
        if abs(diff) < 20 and dist < 600:
            # Random chance to fire if aligned
            if random.random() < 0.05:
                # Fire!
                new_bullets = self.fire()
                if new_bullets:
                    bullets.extend(new_bullets)
        
        return bullets
