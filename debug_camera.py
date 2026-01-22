import arcade
print(dir(arcade.camera))
try:
    print(f"Camera2D exists: {'Camera2D' in dir(arcade.camera)}")
    print(f"Projector exists: {'Projector' in dir(arcade.camera)}")
except:
    pass
