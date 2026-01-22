import arcade

class Shelter(arcade.Sprite):
    def __init__(self, x, y):
        # Using a simple texture for now, maybe a semi-transparent roof
        super().__init__()
        self.center_x = x
        self.center_y = y
        
        # Visual: Gray roof, slightly transparent
        # 64x64 is widely used tile size, or 50x50 based on Wall?
        # Walls seem to be around 50x50 (0.5 scale of tileDirt.png 128px?) -> 64px
        self.texture = arcade.make_soft_square_texture(60, arcade.color.DIM_GRAY, outer_alpha=200)

    def draw(self, **kwargs):
        # Ensure it's drawn, maybe above ground but below tanks? 
        # Actually roofs should be ABOVE tanks if we want to hide them, 
        # but for gameplay clarity, maybe translucent on top is best.
        super().draw(**kwargs)
