# Juego de Tanques 🛡️🔫

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Arcade](https://img.shields.io/badge/Library-Arcade-red)
![Status](https://img.shields.io/badge/Status-Educational-green)

Un juego de combate de tanques para dos jugadores desarrollado en Python con la librería [Arcade](https://api.arcade.academy/).
Este proyecto sirve como base práctica para el **Curso de Python para Desarrollo de Videojuegos**.

## 🚀 Características

*   **Multijugador Local 1v1**: Juega contra un amigo en el mismo teclado.
*   **Sistema de Vida y Munición**: Tanques con 3 vidas y cargadores limitados (5 disparos).
*   **Progresión de Niveles**: 10 mapas de dificultad creciente.
*   **Física Arcade**: Mecánicas de movimiento vectorial y rebote de balas.
*   **Entornos Destruibles**: Rompe muros estratégicamente para alcanzar a tu oponente.
*   **Efectos de Sonido**: Audio inmersivo para disparos, impactos y fin de juego.
*   **Optimizado**: Renderizado de texto eficiente y gestión de sprites.

## 📚 Documentación del Curso

Este repositorio contiene la documentación completa para seguir el curso:

1.  [Indice del Curso](doc/00_indice.md)
2.  [Introducción y Objetivos](doc/01_introduccion.md)
3.  [Configuración del Entorno](doc/02_configuracion.md)
4.  [Arquitectura del Juego](doc/03_arquitectura.md)
5.  [Guía de Código: Paso a Paso](doc/04_codigo_paso_a_paso.md)

## 🛠️ Instalación Rápida

1.  **Clonar el repositorio:**

    ```bash
    git clone <url-del-repositorio>
    cd tanque
    ```

2.  **Configurar entorno virtual:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Jugar:**
    ```bash
    cd game
    python main.py
    ```

## 🎮 Controles

| Acción        | Jugador 1 (Azul) |     Jugador 2 (Rojo)      |
| :------------ | :--------------: | :-----------------------: |
| **Moverse**   |       W, S       |   Flecha Arriba, Abajo    |
| **Girar**     |       A, D       | Flecha Izquierda, Derecha |
| **Disparar**  |        R         |           Enter           |
| **Reiniciar** |     Espacio      |          Espacio          |
| **Salir**     |       Esc        |            Esc            |

## 🧩 Estructura del Proyecto

- `game/`: Código fuente del juego.
- `doc/`: Material educativo del curso.
- `assets/`: Imágenes y sonidos.

---

Desarrollado con ❤️ para aprender Python.
