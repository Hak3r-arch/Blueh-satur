#!/bin/bash
echo "--- INSTALANDO DEPENDENCIAS DE SISTEMA ---"
pkg update && pkg upgrade -y
pkg install python git bluez bluez-utils root-repo -y
pkg install libbluetooth-dev -y
echo "--- INSTALANDO LIBRERIAS DE PYTHON ---"
pip install pybluez2 rich
termux-setup-storage
echo "--- CONFIGURACION COMPLETA. LANZANDO SATURADOR ---"
python flooder.py
