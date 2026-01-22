# Tasks

- [x] Check `tank.py` for deprecated `draw_lrtb_rectangle_filled` usage.
- [x] Verify `maps/` directory and map files exist.
- [x] Run `generate_maps.py` if maps are missing.
- [x] Verify consistent use of `arcade.Text` objects for performance.
- [x] Verify `requirements.txt` is up to date (optional, as it was a previous task).
- [x] Implement Start Menu (Title Screen) as per Architecture documentation.

## Phase 2: Game World & Content
- [x] Map Loader & Level Progression (Verified 10 maps exist)
- [x] Create `PowerUp` class (Shield, Speed, Triple Shot)
- [x] Implement Power-up Spawning (e.g., occasional spawn or from crates)
- [x] Implement Power-up Effects in `Tank` class
- [x] Implement Power-up UI (Visual indicators)

## Phase 3: User Interface & Flow
- [x] Implement Score Tracking (Wins per player)
- [x] Update Game Over screen to show Score
- [x] Add explicit 'Quit' option in Main Menu

## Phase 4: Polish & Juice
- [x] Implement Particle System (Explosions)
- [x] Implement Screen Shake on damage/death
- [x] Add Sound Effects for Power-up pickup
- [x] Add Sound Effects for Damage (if distinct from explosion)

## Phase 5: Lluvia de ácido
- [x] Crear lluvia de ácido que se dispara desde el cielo cuando un tanque recoge un powerup específico para la lluvia de ácido.
- [x] Crear efectos de sonido para la lluvia de ácido.
- [x] Crear efectos visuales para la lluvia de ácido.
- [x] Crear sistema de colisiones para la lluvia de ácido.
- [x] Crear sistema de explosión para la lluvia de ácido.
- [x] Crear lugares donde los tanques pueden protegerse de la lluvia de ácido.

## Phase 6: AI (Bonus)
- [ ] Create simple Bot Logic (Random movement/shooting)
- [ ] Implement pathfinding (A*) if needed (Optional)
- [ ] Allow Single Player vs CPU mode

## Phase 7: Multiplayer (Bonus)
- [ ] Allow Multiplayer mode
- [ ] Implement networking (Optional)
- [ ] Allow Multiplayer vs CPU mode
