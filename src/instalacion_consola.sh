#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # Sin color

echo -e "${GREEN}Iniciando instalación y configuración del proyecto de Consola Retro...${NC}"

# Actualización del sistema
echo -e "${GREEN}Actualizando el sistema...${NC}"
sudo apt update && sudo apt upgrade -y

# Instalación de dependencias
echo -e "${GREEN}Instalando dependencias necesarias...${NC}"
sudo apt install -y xorg openbox xinit python3 python3-tk python3-pip alsa-utils libasound2-dev git curl unzip

# Instalación de bibliotecas Python necesarias
echo -e "${GREEN}Instalando bibliotecas de Python...${NC}"
pip3 install pygame

# Crear directorios necesarios
echo -e "${GREEN}Creando directorios para ROMs y miniaturas...${NC}"
mkdir -p /home/pi/roms/snes /home/pi/roms/snes/thumbnails

# Configuración del sonido
echo -e "${GREEN}Configurando el audio...${NC}"
sudo sed -i '/^dtparam=audio=/c\dtparam=audio=on' /boot/config.txt
amixer cset numid=3 1  # Establecer salida de audio en jack 3.5mm
echo "export SDL_AUDIODRIVER=alsa" >> /home/pi/.bashrc

# Descarga del código fuente del proyecto
echo -e "${GREEN}Clonando el repositorio del proyecto...${NC}"
if [ ! -d "/home/pi/proyecto-consola" ]; then
    git clone https://github.com/usuario/proyecto-consola.git /home/pi/proyecto-consola
else
    echo -e "${RED}El repositorio ya existe en /home/pi/proyecto-consola. Saltando descarga...${NC}"
fi

# Copiar el script principal y configuraciones
echo -e "${GREEN}Copiando el script principal y configuraciones...${NC}"
cp /home/pi/proyecto-consola/gestor_mednafen.py /home/pi/
cp /home/pi/proyecto-consola/iniciar-interfaz.sh /home/pi/
chmod +x /home/pi/iniciar-interfaz.sh

# Configuración del arranque automático con interfaz gráfica
echo -e "${GREEN}Configurando arranque automático para la interfaz gráfica...${NC}"
sudo sed -i '/^exit 0/i su - pi -c "startx /home/pi/iniciar-interfaz.sh"' /etc/rc.local

# Configuración para silenciar mensajes de arranque
echo -e "${GREEN}Silenciando mensajes de arranque...${NC}"
sudo sed -i 's/$/ quiet loglevel=0 splash vt.global_cursor_default=0/' /boot/cmdline.txt

# Configuración de permisos para XServer
echo -e "${GREEN}Configurando permisos para XServer...${NC}"
sudo sed -i '/allowed_users=/c\allowed_users=anybody' /etc/X11/Xwrapper.config

# Configuración de Openbox para arrancar la interfaz
echo -e "${GREEN}Configurando Openbox para iniciar la interfaz gráfica...${NC}"
mkdir -p /home/pi/.config/openbox
echo 'python3 /home/pi/gestor_mednafen.py' > /home/pi/.config/openbox/autostart

# Configuración de Splash Screen (opcional)
echo -e "${GREEN}Configurando pantalla de inicio (Splash Screen)...${NC}"
sudo apt install -y plymouth plymouth-themes
sudo cp /home/pi/proyecto-consola/splash.png /usr/share/plymouth/themes/pix/splash.png

# Reinicio del sistema para aplicar los cambios
echo -e "${GREEN}Instalación completa. Reiniciando el sistema...${NC}"
sudo reboot
