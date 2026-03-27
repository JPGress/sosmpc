import os
import subprocess
from core.net_utils import detect_wifi, run_cmd
from core.config import TUNNEL_PROXMOX_PORT, TUNNEL_PFSENSE_PORT, TUNNEL_SOC_PORT, TUNNEL_PID_FILE

METADATA = {
    "name": "Ativar Túneis Distribuídos OOB SSH via ISP",
    "description": "Cria pontes SSH de tráfego lateral entre o Wi-Fi proxy e a rede MPC.",
    "active": True
}

def run():
    print(f"\n--- {METADATA['name']} ---")
    if os.path.isfile(TUNNEL_PID_FILE):
        with open(TUNNEL_PID_FILE, 'r') as f:
            pid = f.read().strip()
        if run_cmd(['kill', '-0', pid], check=False).returncode == 0:
            print(f"[AVISO] PID Registrado em tabela ({pid}) responde ativo PING/Kernel.")
            print("Para evadir port clashing, destrua este túnel anterior primariamente.")
            return

    wifi_iface = detect_wifi()
    if not wifi_iface:
        print("[ERRO] Wi-Fi de Out-Of-Band local não identificado na host (Missing phy80211).")
        return
        
    res = run_cmd(['ip', '-4', 'addr', 'show', 'dev', wifi_iface], check=False)
    wifi_ip = None
    for line in res.stdout.splitlines():
        if 'inet ' in line:
            wifi_ip = line.split()[1].split('/')[0]
            break
            
    if not wifi_ip:
        print(f"[ERRO] {wifi_iface} encontra-se disconectada (Zero Block IPv4). Tunneling impossibilitado.")
        return
        
    print(f"[INFO] Bounding Address Detectado L2/L3: {wifi_ip}")
    print("[INFO] Backgrounding Fork de Conexão...")
    
    cmd = [
        "ssh", "-fN",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-L", f"{wifi_ip}:{TUNNEL_PROXMOX_PORT}:172.16.160.60:8006",
        "-L", f"{wifi_ip}:{TUNNEL_PFSENSE_PORT}:172.16.160.1:80",
        "-L", f"{wifi_ip}:{TUNNEL_SOC_PORT}:172.16.161.60:80",
        "kali@localhost"
    ]
    
    try:
        subprocess.run(cmd, check=False)
        pgrep_res = run_cmd(['pgrep', '-n', '-f', f"ssh.*{wifi_ip}:{TUNNEL_PROXMOX_PORT}"], check=False)
        pid = pgrep_res.stdout.strip()
        
        if pid:
            with open(TUNNEL_PID_FILE, 'w') as f:
                f.write(pid)
            print(f"[OK] Thread Destacado PID: {pid}")
            print(f"\n  Propague estes links em sua WAN Proxy:")
            print(f"  Proxmox VE      =>   https://{wifi_ip}:{TUNNEL_PROXMOX_PORT}")
            print(f"  pfSense Firewall=>   http://{wifi_ip}:{TUNNEL_PFSENSE_PORT}")
            print(f"  S.O.C           =>   http://{wifi_ip}:{TUNNEL_SOC_PORT}")
        else:
            print("[ERRO] Processo aparentemente executado mas escape na contagem de PID Ocorreu.")
    except Exception as e:
        print(f"[ERRO] SSH Daemon recusou a execução Sub-Shell: {e}")
