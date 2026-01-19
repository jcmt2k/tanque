# 01. Introducción y Objetivos

## El Proyecto: Batalla de Tanques 🛡️🔫

En este curso construiremos (y analizaremos) un juego de combate de tanques para dos jugadores. El objetivo es simple: destruir al tanque enemigo antes de que él te destruya a ti.

### Características del Juego

- **Multijugador Local:** Dos personas juegan en el mismo teclado.
- **Sistema de Combate Táctico:**
    - **Vida:** Los tanques resisten 3 impactos antes de explotar.
    - **Munición:** Cargador de 5 balas. ¡Gestiona tus disparos mientras recargas!
- **Física de Balas:** Las balas rebotan, creando situaciones de riesgo.
- **Mapas Dinámicos:** 10 niveles que cargan desde archivos de texto.
- **Sonido:** Efectos inmersivos y música de fondo.

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

4.  **Lógica de Colisiones y Estado:**
    - Detección de impacto (Bala vs Tanque, Bala vs Muro).
    - Gestión de estado: Vida (`hp`), Munición (`ammo`) y Recarga.

5.  **Carga de Datos (I/O):**
    - Leer archivos de texto para generar mapas (`load_map`).
    - Parsear caracteres (`#`, `B`, `.`) para crear el mundo.

## Tecnologías

- **Python 3.10+**: Lenguaje de programación.
- **Arcade Library**: Framework moderno y fácil de usar para juegos 2D en Python.
