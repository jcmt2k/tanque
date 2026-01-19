import arcade
import math
from constants import *
from tank import Tank
from bullet import Bullet
from terrain import load_map

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

        # Sprite Lists
        self.all_sprites = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.terrain_list = list() # Will be populated
        self.wall_list = arcade.SpriteList()
        # Players
        self.player1 = None
        self.player2 = None
        self.winner = None
        self.current_level = 1

        # UI Text Objects
        self.text_winner = None
        self.text_restart = arcade.Text(
            "Presione ESPACIO para reiniciar",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def setup(self, level=None):
        """Set up the game variables and initialize sprites."""
        if level:
            self.current_level = level
        
        # Safe map loading
        map_file = f"maps/map{self.current_level}.txt"
        try:
             # Basic check if file exists (Arcade might error or Terrain load might handle it)
             # terrain.load_map handles file not found by printing error and returning empty list
             pass
        except:
             pass

        self.all_sprites = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.wall_list = load_map(map_file)
        # Fallback if map fails loading (e.g. if we go beyond 10 and file doesn't exist, though we have 10)
        if not self.wall_list and self.current_level > 1:
             print(f"Map {self.current_level} not found. Resetting to 1.")
             self.current_level = 1
             self.wall_list = load_map("maps/map1.txt")

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
        self.text_winner = arcade.Text(
            f"GANADOR: {self.winner.upper()}!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
        )
        
        # Stop Music
        if self.bgm_player:
            try:
                self.bgm_player.pause() 
            except:
                pass # Handle potential errors if player is already stopped
                
        # Play Game Over Sound
        self.play_sound(self.sound_game_over)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.all_sprites.draw()
        self.bullet_list.draw()
        
        # Draw Health Bars
        self.player1.draw_health_bar()
        self.player2.draw_health_bar()

        if self.winner and self.text_winner:
            self.text_winner.draw()
            self.text_restart.text = f"Nivel {self.current_level} Completado. Presione ESPACIO para Nivel {self.current_level + 1}"
            self.text_restart.draw()

    def on_update(self, delta_time):
        if self.winner:
            return

        self.all_sprites.update(delta_time)
        self.bullet_list.update(delta_time)

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
                    else:
                        bullet.bounce(wall)
                        self.play_sound(self.sound_ricochet)
            
            # Bullet vs Tanks
            if arcade.check_for_collision(bullet, self.player1):
                self.player1.hp -= 1
                self.play_sound(self.sound_hit)
                bullet.kill()
                if self.player1.hp <= 0:
                    self.end_game(COLOR_TANK_2)
            elif arcade.check_for_collision(bullet, self.player2):
                self.player2.hp -= 1
                self.play_sound(self.sound_hit)
                bullet.kill()
                if self.player2.hp <= 0:
                     self.end_game(COLOR_TANK_1)

    def on_key_press(self, key, modifiers):
        # Exit Game
        if key == KEY_EXIT:
            self.close()
            return
        
        # Restart / Next Level
        if self.winner and key == KEY_RESTART:
            self.setup(self.current_level + 1)
            return

        # Player 1 Controls
        if key == KEY_P1_UP:
            self.player1.speed = TANK_SPEED # Inverted input
        elif key == KEY_P1_DOWN:
            self.player1.speed = -TANK_SPEED # Inverted input
        elif key == KEY_P1_LEFT:
            self.player1.angle_speed = TANK_TURN_SPEED # Left
        elif key == KEY_P1_RIGHT:
            self.player1.angle_speed = -TANK_TURN_SPEED # Right
        elif key == KEY_P1_FIRE:
            b = self.player1.fire()
            if b: 
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
            b = self.player2.fire()
            if b: 
                self.bullet_list.append(b)
                self.play_sound(self.sound_shoot)

    def on_key_release(self, key, modifiers):
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
