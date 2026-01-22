import arcade
import arcade.camera

# Mock window to initialize context (needed for Camera creation usually? or maybe not)
# Camera2D usually needs a window context or explicit viewport
window = arcade.Window(800, 600, "Test")
cam = arcade.camera.Camera2D()
print(f"Default position: {cam.position}")
print(f"Default bottom_left: {cam.bottom_left}")
window.close()
