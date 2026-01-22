import arcade
print(f"Arcade Version: {arcade.__version__}")
print("Camera" in dir(arcade))
print("camera" in dir(arcade))

try:
    c = arcade.Camera
    print("arcade.Camera exists")
except AttributeError:
    print("arcade.Camera does NOT exist")

try:
    c = arcade.camera.Camera
    print("arcade.camera.Camera exists")
except:
    print("arcade.camera.Camera does NOT exist")

# Check for viewport functions
print(f"set_viewport exists: {'set_viewport' in dir(arcade)}")
