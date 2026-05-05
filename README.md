
# ⚡ BLUEH-SATUR v4.0 ⚡

Saturador de paquetes Bluetooth para Termux alojado en **arch-hacks**.

---

### 🛠️ INSTALACIÓN PASO A PASO
Copiá y pegá los comandos uno por uno:

1. **Actualizar y dependencias:**
```bash
pkg update && pkg upgrade -y
pkg install python git bluez bluez-utils libbluetooth-dev -y
```

2. **Instalar librerías de Python:**
```bash
pip install rich
pip install pybluez2 --pre
```

3. **Clonar el repositorio:**
```bash
git clone https://github.com/Hak3r-arch/Blueh-satur.git
```

4. **Entrar y ejecutar:**
```bash
cd Blueh-satur
chmod +x arch-hacks
python arch-hacks
```

---

### 🚀 COMPONENTES
- **arch-hacks**: Script principal de saturación.

### 👤 AUTOR: Hak3r-arch

---

### ⚠️ AVISO LEGAL
El autor no se hace responsable por el mal uso de esta herramienta. Uso exclusivo para pruebas de estrés autorizadas.

