
"""
Global constants for the Tank Game.
"""
import arcade

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Juego de Tanques v2 - Professional Edition"

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
POWERUP_TYPE_SHIELD = 0
POWERUP_TYPE_SPEED = 1
POWERUP_TYPE_TRIPLE = 2
POWERUP_DURATION = 10.0 # Seconds
POWERUP_SPAWN_TIME = 15.0 # Seconds
POWERUP_SCALE = 0.5
POWERUP_TYPE_ACID = 3
ACID_RAIN_DURATION = 10.0
ACID_DAMAGE = 0.5
