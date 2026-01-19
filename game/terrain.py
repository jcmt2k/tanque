import arcade
import random
from constants import *


class Block(arcade.Sprite):
    def __init__(self, filename, scale, destructible=False):
        super().__init__(filename, scale)
        self.destructible = destructible

def generate_terrain(count=20):
    """
    Generates a symmetrical map with destructible and indestructible blocks.
    The count parameter is used as a density factor.
    """
    terrain_list = arcade.SpriteList()
    
    # Grid Settings
    GRID_SIZE = 40 # Assuming blocks are roughly 80px * 0.5
    cols = int(SCREEN_WIDTH // GRID_SIZE)
    rows = int(SCREEN_HEIGHT // GRID_SIZE)
    
    # Generate Quadrant 1 (Top-Left)
    quad_cols = cols // 2
    quad_rows = rows // 2
    
    # Track occupied positions to avoid overlaps
    occupied = set()

    # Always add border walls
    for c in range(cols):
        # Top and Bottom
        for r in [0, rows - 1]:
            pos = (c, r)
            if pos not in occupied:
                block = Block(f"{ASSET_PATH}tileGrass.png", 0.5, destructible=False)
                block.center_x = c * GRID_SIZE + GRID_SIZE / 2
                block.center_y = r * GRID_SIZE + GRID_SIZE / 2
                terrain_list.append(block)
                occupied.add(pos)
                
    for r in range(1, rows - 1):
        # Left and Right
        for c in [0, cols - 1]:
            pos = (c, r)
            if pos not in occupied:
                block = Block(f"{ASSET_PATH}tileGrass.png", 0.5, destructible=False)
                block.center_x = c * GRID_SIZE + GRID_SIZE / 2
                block.center_y = r * GRID_SIZE + GRID_SIZE / 2
                terrain_list.append(block)
                occupied.add(pos)

    # Random Obstacles in Quadrant 1
    # We use 'count' to determine how many obstacles to try and place in the quadrant
    # Then we mirror them.
    
    attempts = count * 2 
    for _ in range(attempts):
        c = random.randint(2, quad_cols - 1)
        r = random.randint(2, quad_rows - 1)
        
        # Determine type (30% Indestructible, 70% Destructible)
        if random.random() < 0.3:
            # Indestructible (Steel/Grass)
            filename = f"{ASSET_PATH}tileGrass.png"
            destructible = False
        else:
            # Destructible (Dirt)
            filename = f"{ASSET_PATH}tileDirt.png"
            destructible = True
            
        # Add to all 4 quadrants (Mirroring)
        # Q1: (c, r)
        # Q2: (cols - 1 - c, r)
        # Q3: (c, rows - 1 - r)
        # Q4: (cols - 1 - c, rows - 1 - r)
        
        positions = [
            (c, r),
            (cols - 1 - c, r),
            (c, rows - 1 - r),
            (cols - 1 - c, rows - 1 - r)
        ]
        
        for pos_c, pos_r in positions:
            if (pos_c, pos_r) not in occupied:
                # Don't block the very center spawn areas (approximated)
                # Player 1 starts at ~100, 300 (col ~2, row ~7)
                # Player 2 starts at ~700, 300 (col ~17, row ~7)
                # We can add a simple check if needed, but random luck usually works.
                # Let's enforce a safe zone around spawns if we want, but let's keep it simple.
                
                block = Block(filename, 0.5, destructible=destructible)
                block.center_x = pos_c * GRID_SIZE + GRID_SIZE / 2
                block.center_y = pos_r * GRID_SIZE + GRID_SIZE / 2
                terrain_list.append(block)
                occupied.add((pos_c, pos_r))

    return terrain_list
