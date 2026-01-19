# 02. Configuración del Entorno ⚙️

Antes de empezar a programar o jugar, necesitamos preparar nuestro ordenador.

## Requisitos Previos

- Tener instalado **Python 3.10** o superior.
- Un editor de código (recomendamos VS Code o PyCharm).

## Instalación

1.  **Clonar o Descargar el Proyecto:**
    Mueve la carpeta del proyecto a tu ubicación preferida.

2.  **Crear un Entorno Virtual (Recomendado):**
    Es una buena práctica aislar las librerías del proyecto.

    ```bash
    # En la terminal, dentro de la carpeta del proyecto:
    python3 -m venv .venv

    # Activar el entorno:
    # Linux/Mac:
    source .venv/bin/activate
    # Windows:
    # .venv\Scripts\activate
    ```

3.  **Instalar Dependencias:**
    El archivo `requirements.txt` contiene la lista de librerías necesarias (principalmente `arcade`).
    ```bash
    pip install -r requirements.txt
    ```

## Ejecutar el Juego

Una vez instalado todo, puedes iniciar el juego ejecutando el archivo principal:

```bash
cd game
python main.py
```

### Controles

| Acción        | Jugador 1 (Azul) |     Jugador 2 (Rojo)      |
| :------------ | :--------------: | :-----------------------: |
| **Moverse**   |       W, S       |   Flecha Arriba, Abajo    |
| **Girar**     |       A, D       | Flecha Izquierda, Derecha |
| **Disparar**  |        R         | Enter (Numérico) / Enter  |
| **Reiniciar** |     Espacio      |          Espacio          |
| **Salir**     |       Esc        |            Esc            |
