import os
import time
import subprocess
from core.config import URL_PROXMOX, URL_PFSENSE, URL_SOC

METADATA = {
    "name": "Interface UI: Propagar URIs",
    "description": "Lança requisições automatizadas do Linux Desktop forçando abrimento web iterativo nos três portais principais MPC.",
    "active": True
}

def run():
    print(f"\n--- {METADATA['name']} ---")
    urls = [
        (URL_PROXMOX, "Virtualização Tier-1"),
        (URL_PFSENSE, "Roteador Core Firewall"),
        (URL_SOC, "Auditoria/Log Management")
    ]
    
    # Previne que o sudo abra instâncias X11 limitadas a root travando a renderização visual em Debian/Ubuntu.
    sudo_user = os.environ.get('SUDO_USER')
    
    for url, label in urls:
        print(f"[EXEC] Notificando Desktop Environment ({label}): {url}")
        cmd = ['xdg-open', url]
        if sudo_user:
            cmd = ['sudo', '-u', sudo_user, 'xdg-open', url]
            
        try:
            # Popen garante que thread escape evitando travar em loop esperando browser tab dar Quit.
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"[ERRO X11] Requisição rejeitada GUI-less: {e}")
            
        time.sleep(0.7)
        
    print("\n[OK] Sinais despachados. Olhe as abas em seu Firefox/Chrome principal.")
