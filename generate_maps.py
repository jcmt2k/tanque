
import random
import os

MAP_DIR = "game/maps"
os.makedirs(MAP_DIR, exist_ok=True)

ROWS = 15
COLS = 20

def generate_map(difficulty):
    # Difficulty 1-10
    # Higher difficulty = More steel (#), Less open space, More complex patterns
    
    grid = [['.' for _ in range(COLS)] for _ in range(ROWS)]
    
    # Fill borders
    for r in range(ROWS):
        for c in range(COLS):
            if r == 0 or r == ROWS-1 or c == 0 or c == COLS-1:
                grid[r][c] = '#'
                
    # Internal logic
    # Wall density increases with difficulty
    # Type of wall (Steel vs Brick) ratio shifts towards Steel with difficulty
    
    # Density: 0.1 (Map 1) to 0.4 (Map 10)
    density = 0.1 + (difficulty * 0.03) 
    
    # Steel Probability: 0.2 (Map 1) to 0.6 (Map 10)
    steel_prob = 0.2 + (difficulty * 0.04)
    
    # Pattern Logic
    # 1-3: Random noise / Open
    # 4-7: Lines / Mazes
    # 8-10: Tight grid / Checkerboard
    
    if difficulty <= 3:
        # Random scattering
        for r in range(2, ROWS-2):
            for c in range(2, COLS-2):
                if random.random() < density:
                    grid[r][c] = '#' if random.random() < steel_prob else 'B'
                    
    elif difficulty <= 7:
         # Lines / Maze-ish
        for r in range(2, ROWS-2, 2):
            for c in range(2, COLS-2):
                if random.random() < density * 1.5: # Higher density on lines
                     grid[r][c] = '#' if random.random() < steel_prob else 'B'
        for c in range(4, COLS-4, 4):
            for r in range(2, ROWS-2):
                 if random.random() < density:
                     grid[r][c] = '#' if random.random() < steel_prob else 'B'

    else:
        # Heavy Grid / Choke points
        for r in range(2, ROWS-2):
            for c in range(2, COLS-2):
                 if (r % 2 == 0 and c % 2 == 0) or random.random() < density:
                    grid[r][c] = '#' if random.random() < steel_prob else 'B'

    # Add Shelters (Acid Rain protection)
    # Ensure at least 3-5 shelters per map
    num_shelters = random.randint(3, 6)
    shelters_placed = 0
    attempts = 0
    while shelters_placed < num_shelters and attempts < 100:
        r = random.randint(2, ROWS-3)
        c = random.randint(2, COLS-3)
        if grid[r][c] == '.':
            grid[r][c] = 'S'
            shelters_placed += 1
        attempts += 1

    # Clear spawn zones (Top-Left and Bottom-Right approx)
    # Player 1: ~ (2, 7) - wait, Arcade coords logic.
    # Let's just clear a 3x3 area around likely spawn points visually
    # P1 (Left side), P2 (Right side)
    
    # Clear P1 (Left-Center)
    for r in range(ROWS//2 - 2, ROWS//2 + 2):
        for c in range(1, 4):
            grid[r][c] = '.'
            
    # Clear P2 (Right-Center)
    for r in range(ROWS//2 - 2, ROWS//2 + 2):
        for c in range(COLS-4, COLS-1):
            grid[r][c] = '.'

    return grid

def save_map(grid, map_num):
    filename = os.path.join(MAP_DIR, f"map{map_num}.txt")
    with open(filename, "w") as f:
        for row in grid:
            f.write("".join(row) + "\n")
    print(f"Generated {filename}")

if __name__ == "__main__":
    for i in range(1, 21):
        grid = generate_map(i)
        save_map(grid, i)
