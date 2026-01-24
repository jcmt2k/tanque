
"""
Global constants for the Tank Game.
"""
import arcade

# Screen settings
# Screen settings
GAME_WIDTH = 800
SIDEBAR_WIDTH = 150
SCREEN_WIDTH = GAME_WIDTH + (SIDEBAR_WIDTH * 2) # 1100
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Juego de Tanques v2 - Professional Edition"

# Game Bounds
GAME_LEFT_X = SIDEBAR_WIDTH
GAME_RIGHT_X = SIDEBAR_WIDTH + GAME_WIDTH

# Game settings
GRAVITY = 0
TANK_SPEED = 3
TANK_TURN_SPEED = 2
TANK_SCALE = 0.3
TANK_STARTING_HP = 3 # Hearts
HEALTH_BAR_WIDTH = 40
HEALTH_BAR_HEIGHT = 6
MAX_AMMO = 5
RELOAD_TIME = 2.0 # Seconds
BULLET_SPEED = 10
BULLET_SCALE = 0.3
FIRE_RATE = 30  # Frames between shots
BULLET_OFFSET = 20 # Distance from center to spawn bullet

# Colors
COLOR_TANK_1 = "blue"
COLOR_TANK_2 = "red"

# Asset Paths (Relative to main.py)
ASSET_PATH = "assets/"

# Sound Paths
SOUND_SHOOT = "disparo.wav"
SOUND_EXPLOSION = "explosion.wav"
SOUND_RICOCHET = "rebote.wav"
SOUND_GAME_OVER = "fin_de_juego.wav"
SOUND_BGM = "musica_fondo.wav"
BGM_VOLUME = 1.0

# Control Keys
# Player 1
KEY_P1_UP = arcade.key.W
KEY_P1_DOWN = arcade.key.S
KEY_P1_LEFT = arcade.key.A
KEY_P1_RIGHT = arcade.key.D
KEY_P1_FIRE = arcade.key.R

# Player 2
KEY_P2_UP = arcade.key.UP
KEY_P2_DOWN = arcade.key.DOWN
KEY_P2_LEFT = arcade.key.LEFT
KEY_P2_RIGHT = arcade.key.RIGHT
KEY_P2_FIRE = arcade.key.NUM_ENTER

# General
KEY_RESTART = arcade.key.SPACE
KEY_EXIT = arcade.key.ESCAPE

# Power-ups
# Power-ups
POWERUP_TYPE_SHIELD = 0
POWERUP_TYPE_RAPID_FIRE = 1 # Formerly SPEED
POWERUP_TYPE_TRIPLE = 2
POWERUP_TYPE_ACID = 3

POWERUP_SPAWN_TIME = 15.0 # Seconds
POWERUP_SCALE = 0.5
ACID_RAIN_DURATION = 10.0 # Kept for event logic
ACID_DAMAGE = 0.5 

POWERUP_CONFIG = {
    POWERUP_TYPE_SHIELD: {
        "name": "Shield",
        "color": arcade.color.BLUE,
        "duration": 10.0,
        "radius": 30
    },
    POWERUP_TYPE_RAPID_FIRE: {
        "name": "Rapid Fire",
        "color": arcade.color.YELLOW,
        "duration": 5.0,
        "fire_rate_cooldown": 5, # Frames (vs 30 default)
        "infinite_ammo": True
    },
    POWERUP_TYPE_TRIPLE: {
        "name": "Triple Shot",
        "color": arcade.color.RED,
        "duration": 10.0,
        "spread_angle": 15,
        "bullet_count": 3
    },
    POWERUP_TYPE_ACID: {
        "name": "Acid Rain",
        "color": arcade.color.EMERALD,
        "duration": 10.0,
        "damage": 0.5
    }
}
