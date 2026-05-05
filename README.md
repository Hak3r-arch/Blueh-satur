
# ⚡ BLUEH-SATUR v4.0 ⚡

Herramienta potente de saturación y stress-test para protocolos Bluetooth (L2CAP/RFCOMM), optimizada para entornos Termux.

---

### 🛠️ INSTALACIÓN PASO A PASO
Copiá y pegá estos comandos uno por uno en tu terminal:

1. **Actualizar el sistema:**
```bash
pkg update && pkg upgrade -y
```

2. **Instalar dependencias necesarias:**
```bash
pkg install git python bluez bluez-utils -y
```

3. **Clonar el repositorio:**
```bash
git clone https://github.com/Hak3r-arch/Blueh-satur.git
```

4. **Entrar a la carpeta y dar permisos:**
```bash
cd Blueh-satur
chmod +x setup.sh inundador.py
```

5. **Ejecutar la herramienta:**
```bash
./setup.sh
```

---

### 🚀 CARACTERÍSTICAS
- **Escaneo dinámico:** Localiza dispositivos activos con su dirección MAC y nombre.
- **Flood Selectivo:** Permite atacar objetivos específicos o realizar un flood masivo.
- **Interfaz UI:** Panel de estadísticas en tiempo real (Paquetes enviados, errores, tiempo).
- **Auto-Config:** El script 'setup.sh' instala automáticamente las librerías de Python faltantes.

---

### 👤 AUTOR
Desarrollado por: **Hak3r-arch**

---

### ⚠️ AVISO LEGAL
Esta herramienta ha sido creada con fines estrictamente educativos y para pruebas de penetración autorizadas. El uso de este software contra dispositivos sin el consentimiento previo del propietario es ilegal. El autor no se responsabiliza por el mal uso de esta herramienta.

