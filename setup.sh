#!/bin/bash

echo "--- INICIANDO AUTOMATIZACIÓN DE DEPENDENCIAS ---"

# Actualización e instalación de paquetes de sistema
pkg update && pkg upgrade -y
pkg install python git bluez bluez-utils root-repo libbluetooth-dev -y

# Instalación de librerías de Python
pip install pybluez2 rich

# Configuración de permisos de Termux
termux-setup-storage

# Ejecutar el script de Python automáticamente
echo "--- TODO LISTO. LANZANDO HERRAMIENTA ---"
python flooder.py

