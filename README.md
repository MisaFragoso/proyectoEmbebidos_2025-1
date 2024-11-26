# Proyecto Final: Consola de videojuegos Retro

Fundamentos de Sistemas Embebidos

Autores: 
Fragoso Alarcón Alejandro Misael.
López Muñoz José Luis.
Romero Trujillo Jerson.

Este proyecto transforma tu **Raspberry Pi** en una consola de videojuegos retro totalmente funcional. Puedes navegar entre tus juegos utilizando un mando **DualShock** y disfrutar de una interfaz interactiva que soporta miniaturas de juegos y reproducción de música de fondo.

## Características

- **Soporte para múltiples formatos de ROMs:** `.sfc`, `.smc`, `.gba`, `.fig`, `.zip`.
- **Control por joystick (DualShock):** Navega por el menú, selecciona ROMs.
- **Interfaz gráfica personalizable:** Incluye miniaturas de juegos, música de fondo y un diseño retro.
- **Compatible con Mednafen:** Ejecuta juegos usando este potente emulador.

---

## Requisitos

Antes de usar este proyecto, asegúrate de cumplir con los siguientes requisitos:

### Hardware
- Raspberry Pi (probado en Raspberry Pi 4).
- Controlador **DualShock** conectado por USB.

### Software
- **Raspberry Pi OS (Lite)** instalado.
- Python 3.x con las siguientes bibliotecas:
  - `pygame`
  - `subprocess`
  - `shutil`
  - `os`

### Bibliotecas Adicionales
Estas bibliotecas son necesarias para el funcionamiento de Mednafen y para gestionar las características del emulador:

- `build-essential` -> Para compilación.
- `pkg-config` -> Vincular librerías.
- `zlib1g-dev` -> Para que pueda detectar ROMs en formato ZIP.
- `libsdl2-dev` -> Manejo de gráficos.
- `libpng-dev` -> Manejo de capturas de imagen.
- `portaudio19-dev` -> Salida de audio.
- `libpulse-dev` -> Configuración de sonido.
- `libflac-dev` -> Archivos de audio en formato FLAC.
- `joystick` -> Para detectar mandos.
- `jstest` -> Detección y calibración del joystick.

---

## Instalación

Sigue estos pasos para configurar el proyecto en tu Raspberry Pi:

1. **Clona este repositorio** en tu Raspberry Pi:
       git clone https://github.com/MisaFragoso/proyectoEmbebidos_2025-1.git

2. **Instala las dependencias necesarias**:
       sudo apt update.
       sudo apt install `python3 python3-pip libsdl2-dev libpng-dev portaudio19-dev libpulse-dev libflac-dev zlib1g-dev joystick jstest build-essential pkg-config
       pip3 install pygame`.

Configura Mednafen:

3. **Instala Mednafen**:
       sudo apt install mednafen
       Crea el directorio de ROMs:
       mkdir -p /home/pi/roms/snes/thumbnails

4. **Configura tu mando DualShock**:
       Conecta el mando mediante USB y asegúrate de que sea detectado como js0:
       ls /dev/input/js0

5. **Uso**:
Navega por el menú:

Usa el joystick para desplazarte entre los juegos.
Presiona X para iniciar una ROM.
Presiona ESC para salir del juego y volver al menú.


**Licencia**:
Este proyecto está licenciado bajo la MIT License. Consulta el archivo LICENSE para más información.
