
# ⚡ BLUEH-SATUR v4.0 ⚡

Herramienta profesional de saturación Bluetooth (L2CAP/RFCOMM) optimizada para Termux.

---

### 📋 REQUISITOS DEL SISTEMA
Para que la herramienta funcione correctamente, tu sistema debe tener instalados los siguientes paquetes:

1. **Paquetes de Termux:** `python`, `git`, `bluez`, `bluez-utils`, `libbluetooth-dev`.
2. **Librerías de Python:** `pybluez2`, `rich`.
3. **Permisos:** Acceso al almacenamiento y Bluetooth activado.

---

### 🛠️ INSTALACIÓN Y EJECUCIÓN
Copiá y pegá los comandos en este orden:

1. **Instalar dependencias de sistema:**
```bash
pkg update && pkg upgrade -y
pkg install python git bluez bluez-utils root-repo -y
pkg install libbluetooth-dev -y
```

2. **Instalar librerías de Python:**
```bash
pip install pybluez2 rich
```

3. **Configurar almacenamiento y permisos:**
```bash
termux-setup-storage
```

4. **Clonar y Ejecutar:**
```bash
git clone https://github.com/Hak3r-arch/Blueh-satur.git
cd Blueh-satur
chmod +x setup.sh flooder.py
./setup.sh
```

---

### 🚀 ESTRUCTURA DEL PROYECTO
- **flooder.py:** El núcleo de la herramienta (Script principal).
- **setup.sh:** Automatizador de instalación y arranque.

---

### 👤 AUTOR
Desarrollado por: **Hak3r-arch**

---

### ⚠️ AVISO LEGAL
Uso exclusivo para pruebas en dispositivos propios. El autor no se hace responsable por el uso indebido de esta herramienta.

