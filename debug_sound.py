import arcade
import time
import os

# Create a dummy sound file if needed or use existing
# We'll try to load the existing BGM
SOUND_BGM = "game/assets/musica_fondo.wav"

def main():
    if not os.path.exists(SOUND_BGM):
        print(f"Sound file not found at {SOUND_BGM}")
        return

    print("Loading sound...")
    try:
        sound = arcade.load_sound(SOUND_BGM)
    except Exception as e:
        print(f"Failed to load sound: {e}")
        return

    print("Playing sound...")
    player = sound.play(volume=0.1, loop=True)
    print(f"Player object type: {type(player)}")
    
    time.sleep(1)
    
    if hasattr(player, 'pause'):
        print("Player has 'pause' method.")
        print("Pausing...")
        player.pause()
        time.sleep(1)
        print("Resuming (play)...")
        if hasattr(player, 'play'):
            player.play()
        else:
            print("Player has NO 'play' method.")
    else:
        print("Player has NO 'pause' method.")

    time.sleep(1)
    print("Test complete.")

if __name__ == "__main__":
    main()
