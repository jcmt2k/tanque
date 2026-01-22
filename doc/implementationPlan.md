# Implementation Plan - Phase 5: Acid Rain

## Goal
Implement "Acid Rain" event: A new powerup triggers a global rain effect that damages exposed tanks. Players must seek shelter under new roof structures.

## User Review Required
> [!IMPORTANT]
> - **Game Mechanic**: Acid Rain damages **ALL** tanks not under cover (shelter).
> - **Shelter**: We will add a new map object `Shelter` (visualized as a roof). Map files might need updates to include this, or we'll procedurally generate some for now.
> - **Trigger**: Collecting the Purple Powerup triggers the rain for 10 seconds.

## Proposed Changes
### Constants
#### [game/constants.py](file:///home/julio/prueba/python/juegos/tanque/game/constants.py)
- `POWERUP_TYPE_ACID` (New ID, e.g., 3)
- `ACID_RAIN_DURATION` (10s)
- `ACID_DAMAGE` (0.5 hp per hit?)

### Game Assets & Classes
#### [NEW] [game/acid.py](file:///home/julio/prueba/python/juegos/tanque/game/acid.py)
- `AcidDrop` class (Sprite):
    - Spawns at random X, Top Y.
    - moves down.
    - `update()` handles movement.

#### [NEW] [game/shelter.py](file:///home/julio/prueba/python/juegos/tanque/game/shelter.py)
- `Shelter` class (Sprite):
    - Visual: A semi-transparent "Roof" tile.
    - Function: Tanks colliding with this are "safe".

### Core Logic
#### [game/main.py](file:///home/julio/prueba/python/juegos/tanque/game/main.py)
- **Init**:
    - `self.acid_rain_active` (bool)
    - `self.acid_timer` (float)
    - `self.acid_list` (SpriteList)
    - `self.shelter_list` (SpriteList)
- **Setup**:
    - Spawn manual `Shelter` objects (e.g., in corners or center) since maps don't have them yet.
- **Update**:
    - If `acid_rain_active`:
        - Decrement `acid_timer`.
        - Spawn `AcidDrop` frequently (e.g., 5 per frame).
    - Update `acid_list`.
    - **Collision**:
        - `AcidDrop` vs `Shelter` -> Remove drop (Blocked).
        - `AcidDrop` vs `Tank` ->
            - Check if Tank is colliding with `Shelter` (Safety Check).
            - If NOT safe: Damage Tank, Create particle/fizzle effect, Remove drop.
- **Powerup**:
    - Handle `POWERUP_TYPE_ACID` pickup -> Set `acid_rain_active = True`, reset timer.

## Verification Plan
### Manual Verification
1.  **Trigger**: Collect new powerup. Verify "Acid Rain" visual starts.
2.  **Damage**: Stand in open. Verify taking damage.
3.  **Shelter**: Move under Shelter. Verify NO damage.
4.  **Audio**: Verify rain sound / damage sound.
