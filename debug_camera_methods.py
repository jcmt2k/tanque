import arcade.camera

print("Inspecting Camera2D methods:")
print([m for m in dir(arcade.camera.Camera2D) if not m.startswith("_")])
