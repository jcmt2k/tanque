import arcade
import math
from constants import *
from tank import Tank
from bullet import Bullet
from terrain import load_map
from powerup import PowerUp
from particles import Particle
from acid import AcidDrop
from shelter import Shelter
import random

# Game States
STATE_MENU = 0
STATE_GAME = 1
STATE_GAME_OVER = 2
STATE_PAUSED = 3

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

        self.state = STATE_MENU

        # Sprite Lists
        self.all_sprites = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.terrain_list = list() 
        self.wall_list = arcade.SpriteList()
        self.acid_list = arcade.SpriteList()
        self.shelter_list = arcade.SpriteList()
        
        self.powerup_spawn_timer = POWERUP_SPAWN_TIME
        self.acid_rain_active = False
        self.acid_timer = 0
        
        # Players
        self.player1 = None
        self.player2 = None
        self.winner = None
        self.score_p1 = 0
        self.score_p2 = 0
        self.current_level = 1
        
        
        # Polish
        self.camera = arcade.camera.Camera2D()
        self.shake_amount = 0
        self.particle_list = arcade.SpriteList()

        # UI Text Objects
        self.text_winner = None
        self.text_restart = arcade.Text(
            "Presione ESPACIO para reiniciar",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            width=SCREEN_WIDTH,
            align="center",
            multiline=True
        )
        
        self.text_title = arcade.Text(
            "TANK BATTLE",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.BLACK,
            font_size=50,
            anchor_x="center",
            bold=True
        )
        self.text_instruction = arcade.Text(
            "Presione ENTER para Comenzar",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 20,
            arcade.color.DARK_BLUE,
            font_size=20,
            anchor_x="center",
        )
        
        # Menu dynamic text objects
        self.text_score_menu = arcade.Text(
            "",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 60,
            arcade.color.WHITE,
            font_size=16,
            anchor_x="center"
        )
        self.text_quit_menu = arcade.Text(
            "ESC para Salir",
            SCREEN_WIDTH / 2,
            50,
            arcade.color.GRAY,
            font_size=12,
            anchor_x="center"
        )
        
        # Pause text
        self.text_pause = arcade.Text(
            "PAUSA",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
            anchor_y="center"
        )

    def setup(self, level=None):
        """Set up the game variables and initialize sprites."""
        if level:
            self.current_level = level
        
        # Stop existing music if resetting
        if hasattr(self, 'bgm_player') and self.bgm_player:
            try:
                self.bgm_player.pause()
                self.bgm_player.delete() 
            except:
                pass

        # Safe map loading
        map_file = f"maps/map{self.current_level}.txt"
        try:
             # Basic check if file exists (Arcade might error or Terrain load might handle it)
             pass
        except:
             pass

        self.all_sprites = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()
        self.acid_list = arcade.SpriteList()
        self.shelter_list = arcade.SpriteList()
        
        self.powerup_spawn_timer = POWERUP_SPAWN_TIME
        self.acid_rain_active = False
        self.acid_timer = 0
        
        self.camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.shake_amount = 0
        
        self.wall_list, self.shelter_list = load_map(map_file)
        # Fallback if map fails loading (e.g. if we go beyond 10 and file doesn't exist, though we have 10)
        if not self.wall_list and self.current_level > 1:
             print(f"Map {self.current_level} not found. Resetting to 1.")
             self.current_level = 1
             self.wall_list, self.shelter_list = load_map("maps/map1.txt")

        self.winner = None
        self.text_winner = None

        # Load Sounds
        self.sound_shoot = self.load_sound_safe(SOUND_SHOOT)
        self.sound_hit = self.load_sound_safe(SOUND_EXPLOSION)
        self.sound_ricochet = self.load_sound_safe(SOUND_RICOCHET)
        self.sound_bgm = self.load_sound_safe(SOUND_BGM)
        self.sound_game_over = self.load_sound_safe(SOUND_GAME_OVER)
        
        self.bgm_player = None

        # Play Background Music (Looping)
        if self.sound_bgm:
            self.bgm_player = self.sound_bgm.play(volume=BGM_VOLUME, loop=True)

        # Player 1 (Blue)
        self.player1 = Tank(COLOR_TANK_1, TANK_SCALE)
        self.player1.center_x = 100
        self.player1.center_y = 300
        self.all_sprites.append(self.player1)

        # Player 2 (Red)
        self.player2 = Tank(COLOR_TANK_2, TANK_SCALE)
        self.player2.center_x = 700
        self.player2.center_y = 300
        self.player2.angle = 180
        self.all_sprites.append(self.player2)

    def load_sound_safe(self, filename):
        """Loads a sound safely, returning None if file is missing."""
        try:
            return arcade.load_sound(f"{ASSET_PATH}{filename}")
        except FileNotFoundError:
            print(f"Warning: Sound file '{filename}' not found in {ASSET_PATH}.")
            return None

    def play_sound(self, sound):
        """Plays a sound if it exists."""
        if sound:
            arcade.play_sound(sound)

    def end_game(self, winner):
        """Handles game over state."""
        self.winner = winner
        self.state = STATE_GAME_OVER
        
        if self.winner == COLOR_TANK_1:
            self.score_p1 += 1
        elif self.winner == COLOR_TANK_2:
            self.score_p2 += 1
            
        self.text_winner = arcade.Text(
            f"GANADOR: {self.winner.upper()}!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 30,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
        )
        
        # We'll use text_restart for the score display + restart instruction
        score_text = f"P1 (Blue): {self.score_p1}  -  P2 (Red): {self.score_p2}"
        self.text_restart.text = f"{score_text}\n\n Presione ESPACIO para Siguiente Nivel"
        
        # Stop Music
        if self.bgm_player:
            try:
                self.bgm_player.pause() 
            except:
                pass # Handle potential errors if player is already stopped
                
        # Play Game Over Sound
        self.play_sound(self.sound_game_over)

    def draw_menu(self):
        """Draws the main menu."""
        self.clear()
        self.text_title.draw()
        self.text_instruction.draw()
        
        # Draw Score if not 0-0
        if self.score_p1 > 0 or self.score_p2 > 0:
            self.text_score_menu.text = f"Puntos: Blue {self.score_p1} - Red {self.score_p2}"
            self.text_score_menu.draw()
            
            self.text_score_menu.draw()
            
        self.text_quit_menu.draw()
        
    def create_explosion(self, x, y, color, count=10):
        """Spawns particles for an explosion."""
        for _ in range(count):
            p = Particle(x, y, color)
            self.particle_list.append(p)
        
    def on_draw(self):
        self.clear()
        
        if self.state == STATE_MENU:
            self.draw_menu()
            return
            
        # Use Camera for Shake effect
        self.camera.use()
        
        self.wall_list.draw()
        self.shelter_list.draw()
        self.all_sprites.draw()
        self.bullet_list.draw()
        self.powerup_list.draw()
        self.acid_list.draw()
        self.particle_list.draw()
        
        # Draw Health Bars
        if self.player1: self.player1.draw_health_bar()
        if self.player2: self.player2.draw_health_bar()

        # UI elements should be drawn with a static camera if we had a separate UI camera
        # For now, health bars shake with the world (which is fine/good).
        # Winner text and Pause overlay should NOT shake ideally, but we only have one camera so far.
        # Let's reset camera for UI overlays.
        
        # Reset Viewport for UI (Identity matrix)
        # Note: If we had a self.ui_camera it would be cleaner, but simple reset works too.
        # But wait, arcade.Camera.use() sets viewport. 
        # To draw UI static, we can move camera back to 0,0 temporarily or create a 2nd camera.
        # Let's create a 2nd camera in __init__? Or just rely on the fact that when paused/gameover we probably aren't shaking much.
        # Actually screen shake happens during GAME state. Powerups/Health are world space.
        # Winner Text is Screen Space.
        
        if self.winner and self.text_winner:
             # Reset camera position for static UI text
             # self.camera.move_to((0,0)) # This would affect world if we don't swap back. 
             # Easier to just create a UI camera.
             pass 

        if self.winner and self.text_winner:
            self.text_winner.draw()
            # text_restart now contains the score and instructions, updated in end_game
            self.text_restart.draw()
            
        if self.state == STATE_PAUSED:
            # Full screen overlay
            arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, (0,0,0, 150))
            self.text_pause.draw()

    def on_update(self, delta_time):
        if self.state != STATE_GAME:
            return

        self.all_sprites.update(delta_time)
        self.bullet_list.update(delta_time)
        self.powerup_list.update()
        self.particle_list.update()
        
        # Screen Shake Decay
        if self.shake_amount > 0:
            self.shake_amount -= 0.2
            if self.shake_amount < 0:
                self.shake_amount = 0
            
            # Apply shake to camera
            shake_x = random.uniform(-self.shake_amount, self.shake_amount)
            shake_y = random.uniform(-self.shake_amount, self.shake_amount)
            self.camera.position = (SCREEN_WIDTH / 2 + shake_x, SCREEN_HEIGHT / 2 + shake_y)
        else:
            self.camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # Power-up Spawning
        self.powerup_spawn_timer -= delta_time
        if self.powerup_spawn_timer <= 0:
            self.powerup_spawn_timer = POWERUP_SPAWN_TIME
            # Attempt to spawn powerup
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            
            # Simple check to avoid walls
            p = PowerUp(x, y)
            if not arcade.check_for_collision_with_list(p, self.wall_list):
                 self.powerup_list.append(p)
                 
        # Power-up Collision (Tanks)
        for tank in [self.player1, self.player2]:
            hit_powerups = arcade.check_for_collision_with_list(tank, self.powerup_list)
            for p in hit_powerups:
                tank.apply_powerup(p.type)
                
                # Acid Rain Trigger
                if p.type == POWERUP_TYPE_ACID:
                    self.acid_rain_active = True
                    self.acid_timer = ACID_RAIN_DURATION
                    # Maybe play a thunder sound?
                
                p.remove_from_sprite_lists()
                # Play pickup sound
                self.play_sound(self.sound_ricochet)

        # Acid Rain Logic
        if self.acid_rain_active:
            self.acid_timer -= delta_time
            if self.acid_timer <= 0:
                self.acid_rain_active = False
            else:
                # Spawn drops (e.g., 2 per frame for heavy rain)
                if random.random() < 0.3: # Adjust density
                    drop = AcidDrop(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT)
                    self.acid_list.append(drop)
        
        self.acid_list.update()
        
        # Acid Collision
        for drop in self.acid_list:
            # Hit Shelter?
            if arcade.check_for_collision_with_list(drop, self.shelter_list):
                 drop.remove_from_sprite_lists()
                 continue
                 
            # Hit Tank?
            for tank in [self.player1, self.player2]:
                if arcade.check_for_collision(drop, tank):
                    # Check if tank is under shelter
                    if not arcade.check_for_collision_with_list(tank, self.shelter_list):
                        tank.hp -= ACID_DAMAGE
                        # Visual: Fizzle?
                        self.create_explosion(tank.center_x, tank.center_y, arcade.color.LIME, 5)
                        self.play_sound(self.sound_hit)
                        if tank.hp <= 0:
                             winner = COLOR_TANK_2 if tank == self.player1 else COLOR_TANK_1
                             self.end_game(winner)
                    
                    drop.remove_from_sprite_lists()
                    break # Drop consumed

        # Tank vs Terrain Collision
        for tank in [self.player1, self.player2]:
            if arcade.check_for_collision_with_list(tank, self.wall_list):
                # Simple recoil
                tank.speed *= -0.5
                tank.update() # Move back
                tank.speed = 0

        # Bullet Collisions
        for bullet in self.bullet_list:
            # Bullet vs Walls
            if bullet.collision_cooldown == 0:
                hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
                for wall in hit_list:
                    # Check for destructible wall
                    if hasattr(wall, 'destructible') and wall.destructible:
                        wall.remove_from_sprite_lists()
                        bullet.kill()
                        self.play_sound(self.sound_hit) # Use hit/explosion sound for breaking walls
                        self.create_explosion(wall.center_x, wall.center_y, arcade.color.ORANGE, 15)
                        self.shake_amount = 5
                    else:
                        bullet.bounce(wall)
                        self.play_sound(self.sound_ricochet)
                        self.create_explosion(bullet.center_x, bullet.center_y, arcade.color.GRAY, 5)
            
            # Bullet vs Tanks
            if arcade.check_for_collision(bullet, self.player1):
                if not self.player1.is_shielded:
                    self.player1.hp -= 1
                    self.create_explosion(self.player1.center_x, self.player1.center_y, arcade.color.RED, 20)
                    self.shake_amount = 10
                    self.play_sound(self.sound_hit)
                else:
                    self.play_sound(self.sound_ricochet)

                bullet.kill()
                if self.player1.hp <= 0:
                    self.end_game(COLOR_TANK_2)
            elif arcade.check_for_collision(bullet, self.player2):
                if not self.player2.is_shielded:
                    self.player2.hp -= 1
                    self.create_explosion(self.player2.center_x, self.player2.center_y, arcade.color.BLUE, 20)
                    self.shake_amount = 10
                    self.play_sound(self.sound_hit)
                else:
                    self.play_sound(self.sound_ricochet)

                bullet.kill()
                if self.player2.hp <= 0:
                     self.end_game(COLOR_TANK_1)

    def on_key_press(self, key, modifiers):
        # Exit Game
        if key == KEY_EXIT:
            self.close()
            return

        if self.state == STATE_MENU:
            if key == arcade.key.ENTER:
                self.setup(1)
                self.state = STATE_GAME
            return
        
        # Restart / Next Level
        if self.state == STATE_GAME_OVER and key == KEY_RESTART:
            self.setup(self.current_level + 1)
            self.state = STATE_GAME
            return

        # Pause Toggle
        if key == arcade.key.P:
            if self.state == STATE_GAME:
                self.state = STATE_PAUSED
                if self.bgm_player:
                    self.bgm_player.pause()
            elif self.state == STATE_PAUSED:
                self.state = STATE_GAME
                if self.bgm_player:
                    self.bgm_player.play()
            return
            
        # Player 1 Controls (Only in GAME state)
        if self.state == STATE_GAME:
            if key == KEY_P1_UP:
                self.player1.speed = TANK_SPEED # Inverted input
            elif key == KEY_P1_DOWN:
                self.player1.speed = -TANK_SPEED # Inverted input
            elif key == KEY_P1_LEFT:
                self.player1.angle_speed = TANK_TURN_SPEED # Left
            elif key == KEY_P1_RIGHT:
                self.player1.angle_speed = -TANK_TURN_SPEED # Right
            elif key == KEY_P1_FIRE:
                bullets = self.player1.fire()
                if bullets: 
                    for b in bullets:
                        self.bullet_list.append(b)
                    self.play_sound(self.sound_shoot)
    
            # Player 2 Controls
            if key == KEY_P2_UP:
                self.player2.speed = TANK_SPEED # Inverted input
            elif key == KEY_P2_DOWN:
                self.player2.speed = -TANK_SPEED # Inverted input
            elif key == KEY_P2_LEFT:
                self.player2.angle_speed = TANK_TURN_SPEED # Left
            elif key == KEY_P2_RIGHT:
                self.player2.angle_speed = -TANK_TURN_SPEED # Right
            elif key == KEY_P2_FIRE:
                bullets = self.player2.fire()
                if bullets: 
                    for b in bullets:
                        self.bullet_list.append(b)
                    self.play_sound(self.sound_shoot)

    def on_key_release(self, key, modifiers):
        if self.state != STATE_GAME:
            return

        # Player 1 Stop
        if key in (KEY_P1_UP, KEY_P1_DOWN):
            self.player1.speed = 0
        elif key in (KEY_P1_LEFT, KEY_P1_RIGHT):
            self.player1.angle_speed = 0
        
        # Player 2 Stop
        if key in (KEY_P2_UP, KEY_P2_DOWN):
            self.player2.speed = 0
        elif key in (KEY_P2_LEFT, KEY_P2_RIGHT):
            self.player2.angle_speed = 0

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
