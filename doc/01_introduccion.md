# 01. Introducción y Objetivos

## El Proyecto: Batalla de Tanques 🛡️🔫

En este curso construiremos (y analizaremos) un juego de combate de tanques para dos jugadores. El objetivo es simple: destruir al tanque enemigo antes de que él te destruya a ti.

### Características del Juego

- **Multijugador Local:** Dos personas juegan en el mismo teclado.
- **Física de Balas:** Las balas rebotan en las paredes.
- **Terreno Destruible:** Algunos obstáculos pueden ser destruidos con disparos.
- **Sonido:** Efectos de disparos, explosiones y música de fondo.

## Objetivos de Aprendizaje 🧠

Usando este juego como ejemplo, exploraremos conceptos clave de la programación moderna y el desarrollo de software:

1.  **Programación Orientada a Objetos (POO):**
    - Uso de **Clases** para representar entidades del juego (`Tank`, `Bullet`, `Block`).
    - **Herencia** para reutilizar código de la librería Arcade (`arcade.Sprite`).
    - **Encapsulamiento** de lógica específica (ej. el tanque sabe cómo moverse, la bala sabe cómo rebotar).

2.  **El Bucle de Juego (Game Loop):**
    - Entender cómo funcionan los videojuegos en tiempo real: `Input` -> `Update` -> `Draw`.
    - Manejo de tiempos (`delta_time`) para movimiento fluido.

3.  **Matemáticas Básicas para Juegos:**
    - Uso de **Trigonometría** (Seno y Coseno) para calcular vectores de movimiento basados en un ángulo.
    - Sistema de coordenadas cartesiano.

4.  **Lógica de Colisiones:**
    - Detección de impacto entre objetos.
    - Reacción a colisiones (rebotar, destruir, detenerse).

## Tecnologías

- **Python 3.10+**: Lenguaje de programación.
- **Arcade Library**: Framework moderno y fácil de usar para juegos 2D en Python.
