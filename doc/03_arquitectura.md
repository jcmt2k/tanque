# 03. Arquitectura del Juego 🏗️

Entender cómo está organizado el código es fundamental para poder modificarlo o expandirlo. A continuación, desglozamos la estructura del proyecto.

## Estructura de Archivos

```text
/game
├── main.py        # PUNTO DE ENTRADA. Contiene la clase principal `MyGame` y el bucle de juego.
├── constants.py   # Variables globales (Configuración, Colores, Rutas, Teclas).
├── tank.py        # Clase `Tank`: Lógica del jugador (movimiento, disparo).
├── bullet.py      # Clase `Bullet`: Lógica de los proyectiles (movimiento, rebote).
├── terrain.py     # Generación procedural del mapa y clase `Block`.
└── assets/        # Carpeta con imágenes y sonidos.
```

## Diagrama de Clases (Simplificado)

El juego utiliza **Herencia** de la clase `arcade.Sprite` para casi todos los objetos visibles.

- **`arcade.Window`**
  - `MyGame`: Controlador principal. Maneja el estado (Menú, Juego, Fin), los eventos de teclado y el dibujado.

- **`arcade.Sprite`**
  - `Tank`: Añade propiedades de velocidad, cooldown de disparo y métodos para moverse vectorialmente.
  - `Bullet`: Añade lógica de rebote y tiempo de vida.
  - `Block`: Añade propiedad de `destructible`.

## El Bucle de Juego (The Game Loop)

Arcade se encarga de llamar a tres métodos principales en `MyGame` muchas veces por segundo (aprox. 60 veces/seg):

1.  **`on_key_press` / `on_key_release`**:
    - Detecta cuándo pulsamos teclas.
    - **NO** muevas el tanque aquí. Aquí solo cambiamos el _estado_ del tanque (ej. `tank.speed = 5`).

2.  **`on_update(delta_time)`**:
    - Aquí es donde ocurre la magia.
    - Se actualizan las posiciones (`self.all_sprites.update()`).
    - Se comprueban colisiones (`arcade.check_for_collision`).
    - Se aplica la lógica de juego (¿Alguien ganó? ¿Murió una bala?).

3.  **`on_draw()`**:
    - Limpia la pantalla.
    - Dibuja todo en su nueva posición.
