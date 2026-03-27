from core.config import C
import glob
from core.net_utils import detect_eth, detect_wifi, run_cmd

METADATA = {
    "name": "Status Transparente de Redes/Interfaces",
    "description": "Dá 'Dump' formatado sobre endereçamento IPv4, roteamento e detecção de BKP.",
    "active": True
}

def run():
    print(f'\n{C.BOLD}--- {METADATA[\"name\"]} ---{C.RESET}')
    
    try:
        eth_iface = detect_eth()
    except Exception:
        eth_iface = "N/A"
        
    try:
        wifi_iface = detect_wifi()
    except Exception:
        wifi_iface = "N/A"
        
    print(f"\n>> Ethernet Cabeada L3 ({eth_iface}) <<")
    if eth_iface != "N/A":
        res = run_cmd(['ip', '-4', 'addr', 'show', 'dev', eth_iface], check=False)
        if res.stdout.strip():
            print(res.stdout.strip())
        else:
            print("  Sem endereço IPv4 dinâmico/estático detectado.")
            
        print("\n  [Rotas de Roteador Atuantes]")
        r_res = run_cmd(['ip', 'route', 'show', 'dev', eth_iface], check=False)
        print("  " + r_res.stdout.strip() if r_res.stdout.strip() else "  (Nenhuma Atrelada)")
        
    print(f"\n>> Wi-Fi Gateway Local ISP ({wifi_iface}) <<")
    if wifi_iface and wifi_iface != "N/A":
        res = run_cmd(['ip', '-4', 'addr', 'show', 'dev', wifi_iface], check=False)
        if res.stdout.strip():
            print(res.stdout.strip())
        else:
            print("  WLAN Sem range IP.")
            
        print("\n  [Rota Default (Ponta WAN)]")
        r_res = run_cmd(['ip', 'route', 'show', 'default', 'dev', wifi_iface], check=False)
        print("  " + r_res.stdout.strip() if r_res.stdout.strip() else "  Desconectada Externamente.")
        
    print("\n>> Respositório de Caches (Backups em RAMDisk) <<")
    if eth_iface != "N/A":
        backups = glob.glob(f"/tmp/eth_backup_{eth_iface}_*.conf")
        if backups:
            for bkp in backups:
                print(f"  {bkp}")
        else:
            print("  [INFO] Diretório sem backups nativos para a placa informada.")
    else:
        print("  Ethernet Física faltante.")
