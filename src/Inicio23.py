import pygame
import os
import subprocess
import time

# Configuración de la pantalla y colores
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
BLACK, WHITE, RED, GREEN, YELLOW = (0, 0, 0), (255, 255, 255), (200, 50, 50), (50, 200, 50), (255, 255, 0)

# Inicializar Pygame
pygame.init()

# Hacer visible el cursor
pygame.mouse.set_visible(True)

# Cargar música de fondo
pygame.mixer.init()
pygame.mixer.music.load("SonidoFondo.mp3")  # Cambia el archivo por tu música

# Cargar sonidos de efectos
select_sound = pygame.mixer.Sound("SonidoMenu.mp3")  # Sonido para seleccionar
launch_sound = pygame.mixer.Sound("SonidoSeleccion.mp3")  # Sonido al lanzar juego
start_sound = pygame.mixer.Sound("SonidoInicio.mp3")  # Sonido de inicio

# Configuración de la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Retro Emulador")

# Cargar imagen de fondo
background_image = pygame.image.load("ImagenFondo.jpg").convert()

# Cargar y escalar la imagen de inicio
splash_image = pygame.image.load("InicioConsola.jpg").convert()
splash_image = pygame.transform.scale(splash_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Ajustar tamaño

# Cargar fuente personalizada
font = pygame.font.Font("FuenteConsola.ttf", 24)  # Cambia la fuente si necesitas

# Configuración del joystick
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Mando detectado: {joystick.get_name()}")

# Directorio de las ROMs y miniaturas
ROMS_DIR = "/home/pi/roms/snes"
THUMBNAILS_DIR = os.path.join(ROMS_DIR, "thumbnails")

# Cargar las ROMs y limpiar sus nombres
roms = [f for f in os.listdir(ROMS_DIR) if f.endswith(('.sfc', '.smc', '.gba', '.fig', '.zip'))]
clean_rom_names = [
    os.path.splitext(rom)[0].replace("_", " ").replace(".", " ") for rom in roms
]  # Eliminar extensiones y limpiar nombres

# Cargar las miniaturas asociadas a las ROMs
thumbnails = {
    rom: pygame.image.load(os.path.join(THUMBNAILS_DIR, os.path.splitext(rom)[0] + ".png")).convert_alpha()
    if os.path.exists(os.path.join(THUMBNAILS_DIR, os.path.splitext(rom)[0] + ".png"))
    else None
    for rom in roms
}

# Variables para el menú
selected_index = 0
running = True

# Altura máxima permitida para el listado de ROMs
max_roms_display = (SCREEN_HEIGHT - 200) // 40  # 40 es el espacio vertical por ROM

# Posición y dimensiones del botón de salir
# exit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 60, 200, 50)


def show_splash_screen():
    """Muestra una imagen de inicio con sonido."""
    screen.fill(BLACK)
    screen.blit(splash_image, (0, 0))  # Dibujar la imagen de inicio escalada
    pygame.display.flip()

    # Reproducir el sonido de inicio
    start_sound.play()

    # Esperar 3 segundos o hasta que el sonido termine
    time.sleep(3)


def draw_menu():
    """Dibuja el menú con las ROMs disponibles."""
    screen.blit(background_image, (0, 0))  # Dibujar la imagen de fondo

    # Dibujar el título
    title = font.render("Selecciona un Juego", True, YELLOW)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    # Dibujar las ROMs disponibles con miniaturas
    if roms:
        start_index = max(0, selected_index - max_roms_display + 1)  # Desplazar si hay muchas ROMs
        for i, (rom_name, rom) in enumerate(zip(clean_rom_names[start_index:start_index + max_roms_display],
                                                roms[start_index:start_index + max_roms_display])):
            color = RED if i + start_index == selected_index else WHITE
            rom_text = font.render(rom_name, True, color)
            screen.blit(rom_text, (200, 100 + i * 40))  # Texto de la ROM

            # Dibujar la miniatura si existe
            if thumbnails[rom]:
                thumbnail = pygame.transform.scale(thumbnails[rom], (40, 40))  # Escalar la miniatura
                screen.blit(thumbnail, (140, 100 + i * 40))  # Dibujar miniatura junto al nombre
    else:
        # Mostrar un mensaje si no hay ROMs
        no_roms_text = font.render("No se encontraron ROMs.", True, RED)
        screen.blit(no_roms_text, (SCREEN_WIDTH // 2 - no_roms_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # # Dibujar el botón de salir
    # button_color = GREEN if not exit_button_rect.collidepoint(pygame.mouse.get_pos()) else YELLOW
    # pygame.draw.rect(screen, button_color, exit_button_rect)
    # exit_text = font.render("Salir", True, BLACK)
    # screen.blit(exit_text, (exit_button_rect.x + exit_button_rect.width // 2 - exit_text.get_width() // 2,
    #                         exit_button_rect.y + exit_button_rect.height // 2 - exit_text.get_height() // 2))

    pygame.display.flip()


def launch_game(rom):
    """Ejecuta el juego seleccionado usando Mednafen."""
    screen.fill(BLACK)
    loading_text = font.render("Cargando juego...", True, WHITE)
    screen.blit(loading_text, (SCREEN_WIDTH // 2 - loading_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # Pausar la música de fondo
    pygame.mixer.music.pause()

    launch_sound.play()  # Reproducir sonido al lanzar el juego

    try:
        # Ejecutar el juego como un proceso bloqueante
        process = subprocess.Popen(["mednafen", os.path.join(ROMS_DIR, rom)])
        process.wait()  # Esperar a que el juego termine
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el juego: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    # Reanudar la música de fondo
    pygame.mixer.music.unpause()

    # Recuperar el enfoque y reiniciar la pantalla después de cerrar el juego
    pygame.event.clear()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Retro Emulador")


# Mostrar la pantalla de inicio antes del menú
show_splash_screen()

# Iniciar la música de fondo después de la pantalla de inicio
pygame.mixer.music.play(-1)

# Bucle principal
while running:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     # Manejar clic en el botón de salir
        #     if exit_button_rect.collidepoint(event.pos):
        #         print("Botón de salir presionado.")
        #         running = False

        if event.type == pygame.JOYAXISMOTION:
            # Control del stick izquierdo
            if event.axis == 1:  # Eje vertical
                if event.value < -0.9999:  # Mover hacia arriba
                    selected_index = (selected_index - 1) % len(roms)
                    select_sound.play()
                elif event.value > 0.9999:  # Mover hacia abajo
                    selected_index = (selected_index + 1) % len(roms)
                    select_sound.play()

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # Botón X para lanzar el juego
                launch_game(roms[selected_index])
            elif event.button == 1:  # Botón O para salir
                running = False

pygame.quit()
