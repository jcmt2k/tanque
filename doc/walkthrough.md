# Walkthrough - Arcade Compatibility & Map Verification

## Work Accomplished
- Investigated `tank.py` drawing functions.
- Verified map assets in `game/maps/`.
- Verified `arcade.Text` usage for performance.

## Key Findings
- **Arcade API Anomaly**: The installed version of Arcade uses `draw_lrbt_rectangle_filled` (Left-Right-Bottom-Top) instead of the standard `draw_lrtb_rectangle_filled`. The code in `tank.py` correctly matches this environment.
    - *Action Taken*: Reverted an initial attempt to change this to `lrtb`, ensuring the game remains playable in the current environment.
- **Map System**: 
    - 10 Map files exist in `game/maps/`.
    - Loading logic in `terrain.py` appears correct for running from the `game/` directory.

## Verified Files
- `game/tank.py` (Confirmed correct API usage for this env)
- `game/maps/` (Confirmed 10 map files)

## Next Steps
- Run the game using `cd game && python main.py`.

# Walkthrough - Start Menu Implementation

## Work Accomplished
- **State Machine**: Implemented `STATE_MENU` (0), `STATE_GAME` (1), and `STATE_GAME_OVER` (2).
- **Title Screen**: Added a "TANK BATTLE" title screen with "Press ENTER to Start" instruction.
- **Input Handling**: 
    - Separated input logic for Menu and Game.
    - Guarded `on_key_release` to prevent errors when game is not active.
- **Game Over Update**: Integrated Game Over logic into the state machine, allowing clean restarts.

## Verification
- **Syntax Check**: `main.py` compiles successfully.
- **Logic Review**: 
    - Input controls are strictly scoped to the active state.
    - Game loop only updates sprites when in `STATE_GAME`.

## Bug Fix - Tank Controls
- **Issue**: Player 2 controls (Down, Left, Right, Fire) were unresponsive after Start Menu implementation.
- **Root Cause**: Indentation error in `on_key_press` caused P2 controls to be treated as `elif` branches of the `state` check, making them unreachable in `STATE_GAME`.
- **Fix**: Corrected indentation to nest P2 controls inside the `if self.state == STATE_GAME:` block.

# Walkthrough - Phase 2: Power-ups

## Work Accomplished
- **Architecture**:
    - Created `game/powerup.py` with `PowerUp` class.
    - Added constants for types (SHIELD, SPEED, TRIPLE) and duration (10s).
- **Tank Logic**:
    - Updated `Tank` class to track power-up status and timers.
    - Implemented effects:
        - **Speed**: Increases max speed by 50%.
        - **Triple**: Firing spawns 3 bullets in a spread.
        - **Shield**: Visual cyan ring (Damage logic needs `main.py` integration).
- **Game Loop**:
    - Power-ups spawn randomly every 15 seconds in valid locations.
    - Collision detection triggers `apply_powerup` on tanks.
    - Updated `fire()` handling in `main.py` to support multi-bullet return.

## Logic Review
- Spawning ensures no collision with walls.
- Timers automatically expire effects.
- Triple shot utilizes the existing bullet collision logic.

# Walkthrough - Phase 3: UI & Flow

## Work Accomplished
- **Pause System**:
    - Added `STATE_PAUSED` (3).
    - Checks for 'P' key to toggle state.
    - Draws semi-transparent overlay and "PAUSA" text.
    - Game loop halts updates while paused.
- **Score Tracking**:
    - Added persistent score counters `score_p1` and `score_p2` in `active_window`.
    - Scores persist across rounds (until application close).
    - Displayed in Main Menu and Game Over screens.
- **Menu Updates**:
    - Added "ESC to Quit" instructions.
    - Displays current session score.

## Logic Review
- Pause logic correctly interrupts updates and handles Resume.
- Score increments correctly on win condition and survives level restarts (as `__init__` is not re-called, `setup` is).

## Bug Fix - Crash & Performance
- **Issues**:
    - `AttributeError` due to `draw_rectangle_filled` being missing (or renamed) in current Arcade version.
    - `PerformanceWarning` from dynamic `draw_text` usage in Menu and Pause screens.
- **Fixes**:
    - Replaced `draw_rectangle_filled` with `draw_lrbt_rectangle_filled` for the Pause overlay.
    - Converted all dynamic `draw_text` usage to persistent `arcade.Text` objects initialized once.

## Bug Fix - Pause Audio & Text Wrap
- **Issues**:
    - Music continued playing when paused.
    - "Next Level" text did not wrap to a new line as intended.
- **Fixes**:
    - Pausing toggles `bgm_player.pause()` / `bgm_player.play()`.
    - Configured `text_restart` with `multiline=True`, `width=SCREEN_WIDTH`, `align="center"` to support newline characters.
    - Fixed specific bug where music stream was not stopped on restart, causing unpausible background audio. `setup()` now actively stops existing player.

# Walkthrough - Phase 4: Polish & Juice

## Work Accomplished
- **Particle System**:
    - Created `Particle` class in `particles.py`.
    - Implemented `create_explosion` in `main.py` to spawn colored particles with random velocity and fade.
- **Screen Shake**:
    - Implemented camera shake using `arcade.Camera`.
    - `shake_amount` increases on impact and decays over time in `on_update`.
- **Audio Effects**:
    - Added sound feedback for Power-up pickups (`sound_ricochet` reused).
    - Added impact sounds for wall collisions (`sound_hit`).

## Triggers
- **Bullet vs Wall**: Small orange explosion + slight screen shake.
- **Bullet vs Tank**: Large colored explosion (Red/Blue) + heavy screen shake.
- **Powerup Pickup**: Audio feedback.

# Walkthrough - Phase 5: Acid Rain (Lluvia de ácido)

## Work Accomplished
- **Core Mechanics**:
    - Implemented `AcidDrop` class (falling green rain).
    - Implemented `Shelter` class (protective roof structure).
    - Added "Acid Rain" Event triggered by a new **Green Powerup** (Type 3).
- **Map Update**:
    - Modified `terrain.py` to parse 'S' characters as Shelters.
    - Updated `maps/map1.txt` to include 4 Shelter locations.
- **Game Logic**:
    - **Trigger**: Picking up the Acid Powerup starts rain for 10 seconds.
    - **Damage**: Rain deals 0.5 HP damage to any tank *not* colliding with a Shelter.
    - **Visuals**: Raindrops fall from the sky; fizzle explosion on impact.

## Verification
- **Compilation**: `main.py` compiles successfully.
- **Manual Test Steps**:
    1.  Play the game.
    2.  Find/Wait for a **Green Powerup** (Acid).
    3.  Collect it -> Verify rain starts.
    4.  Stand in open -> Take damage (observe health bar drop).
    5.  Move under a grey/transparent Roof (Shelter) -> Verify safety.
