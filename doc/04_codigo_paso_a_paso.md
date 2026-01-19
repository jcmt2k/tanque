# 04. Guía de Código: Paso a Paso 👣

Vamos a analizar las partes más interesantes del código.

## 1. Movimiento Vectorial (`tank.py`)

¿Cómo hacemos que el tanque se mueva en la dirección que mira? Usamos **Trigonometría**.

```python
# tank.py
def update(self):
    # Convertimos el ángulo a radianes (Python usa radianes, Arcade usa grados)
    angle_rad = math.radians(self.angle)

    # Calculamos cuánto movernos en X e Y
    # Seno del ángulo para X, Coseno del ángulo para Y
    self.change_x = math.sin(angle_rad) * self.speed
    self.change_y = math.cos(angle_rad) * self.speed

    super().update() # Aplica: x += change_x, y += change_y
```

> **Reto:** ¿Por qué usamos Sin para X y Cos para Y? En matemáticas estándar suele ser al revés. _Pista: En Arcade, 0 grados es "Arriba" (Norte), no "Derecha" (Este)._

## 2. Rebote de Balas (`bullet.py`)

Para que las balas reboten, necesitamos saber si golpearon una pared horizontal o verticalmente. Una aproximación simple es verificar la superposición:

```python
# bullet.py
def bounce(self, wall):
    # Si el centro de la bala está fuera de los límites horizontales del muro...
    if self.center_x < wall.left or self.center_x > wall.right:
         self.change_x *= -1  # Invertir X (Rebote lateral)

    # Si no, asumimos que fue un golpe vertical...
    else: # self.center_y < wall.bottom or ...
        self.change_y *= -1   # Invertir Y (Rebote techo/suelo)
```

## 3. Gestión de Colisiones (`main.py`)

En `on_update`, comprobamos si las balas tocan algo.

```python
# main.py
hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)

for wall in hit_list:
    if wall.destructible:
        wall.kill()   # Destruir muro
        bullet.kill() # Destruir bala
    else:
        bullet.bounce(wall) # Rebotar
```

## 4. Texto Optimizado (`main.py`)

_Nota: Esto fue parte de una optimización reciente._

Dibujar texto es costoso para la CPU. En lugar de usar `arcade.draw_text` dentro del bucle rápido, creamos objetos `arcade.Text` una sola vez y llamamos a su método `.draw()`.

```python
# main.py
# Bien (En __init__ o al ganar):
self.text_winner = arcade.Text("GANADOR!", ...)

# Bien (En on_draw):
self.text_winner.draw()
# Bien (En on_draw):
self.text_winner.draw()
```

## 5. Cargador de Niveles (`terrain.py`)

Una de las características más potentes es la capacidad de diseñar niveles en texto plano.

**map1.txt**:
```text
##########
#...B....#
#...#....#
##########
```

El código lee este archivo línea por línea y carácter por carácter:

```python
# terrain.py
def load_map(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            # Calculamos posición X, Y según la fila y columna
            x = col_idx * GRID_SIZE
            y = SCREEN_HEIGHT - (row_idx * GRID_SIZE)
            
            if char == '#':
                # Crear Muro Indestructible
            elif char == 'B':
                # Crear Muro Destructible
```

Esto nos permite crear **10 niveles** simplemente editando archivos de texto, sin tocar el código Python.
