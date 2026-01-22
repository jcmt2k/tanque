import arcade
import random
from constants import *


class Block(arcade.Sprite):
    def __init__(self, filename, scale, destructible=False):
        super().__init__(filename, scale)
        self.destructible = destructible

from shelter import Shelter

def load_map(filename):
    """
    Loads a map from a text file.
    Legend:
    # : Indestructible Wall (Grass/Steel visual)
    B : Destructible Wall (Dirt/Brick visual)
    S : Shelter (Protects from Acid Rain)
    . : Empty Space
    """
    terrain_list = arcade.SpriteList()
    shelter_list = arcade.SpriteList()
    GRID_SIZE = 40 
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Map file '{filename}' not found.")
        return terrain_list, shelter_list

    # Calculate offset to center the map if it's smaller, or just start from 0,0
    # Assuming map is designed for 800x600 (20x15 blocks of 40px)
    
    # Iterate rows (top to bottom in file)
    # But coordinate 0 is bottom. So we read file line 0 -> Max Y
    # Actually, let's reverse the lines so line 0 of file is at the top of screen.
    
    total_rows = len(lines)
    
    for row_idx, line in enumerate(lines):
        # We want the first line of the file to be at the TOP of the screen
        # y = SCREEN_HEIGHT - (row_idx * GRID_SIZE) - GRID_SIZE/2
        
        # Or using standard grid coordinates:
        # r = (total_rows - 1) - row_idx
        
        line = line.strip()
        for col_idx, char in enumerate(line):
            x = col_idx * GRID_SIZE + GRID_SIZE / 2
            # Top-down positioning
            y = SCREEN_HEIGHT - (row_idx * GRID_SIZE) - GRID_SIZE / 2
            
            block = None
            if char == '#':
                # Indestructible
                block = Block(f"{ASSET_PATH}tileGrass.png", 0.5, destructible=False)
                block.center_x = x
                block.center_y = y
                terrain_list.append(block)
            elif char == 'B':
                # Destructible
                block = Block(f"{ASSET_PATH}tileDirt.png", 0.5, destructible=True)
                block.center_x = x
                block.center_y = y
                terrain_list.append(block)
            elif char == 'S':
                # Shelter
                s = Shelter(x, y)
                shelter_list.append(s)
                
    return terrain_list, shelter_list
