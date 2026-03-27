import os
import time
from datetime import datetime
from core.net_utils import check_root, run_cmd, detect_eth, detect_wifi, get_wifi_default_route
from core.config import MPC_IP, MPC_PREFIX, MPC_GW, MPC_ROUTES

METADATA = {
    "name": "Aplicar Configuração MPC (Dual-NIC completa)",
    "description": "Configura a interface Ethernet (cabo) para acesso ao ambiente MPC preservando a rota default (Wi-Fi).",
    "active": True
}

def backup_eth(iface):
    timestamp = int(time.time())
    backup_file = f"/tmp/eth_backup_{iface}_{timestamp}.conf"
    
    ips = run_cmd(['ip', '-4', 'addr', 'show', iface]).stdout
    ip_list = [line.split()[1] for line in ips.splitlines() if 'inet ' in line]
    
    routes = run_cmd(['ip', 'route', 'show', 'dev', iface]).stdout
    r_list = [r.strip() for r in routes.splitlines()]
    
    with open(backup_file, 'w') as f:
        f.write(f"IFACE={iface}\n")
        f.write(f"IPS={' '.join(ip_list)}\n")
        f.write(f"ROUTES={'|'.join(r_list)}\n")
        
    print(f"[INFO] Backup salvo temporariamente em: {backup_file}")

def run():
    print(f"\n--- {METADATA['name']} ---")
    if not check_root():
        print("[ERRO] Este módulo altera camadas de roteamento e exige 'sudo'. Acesso negado.")
        return
        
    try:
        eth_iface = detect_eth()
        wifi_iface = detect_wifi()
        wifi_gw = get_wifi_default_route(wifi_iface)
        
        print(f"[INFO] Ethernet : {eth_iface}")
        print(f"[INFO] Wi-Fi    : {wifi_iface or 'N/A'}")
        if wifi_gw:
            print(f"[INFO] Gateway ISP: {wifi_gw}")
            
        backup_eth(eth_iface)
        
        print(f"\n[INFO] Despejando endereços conflitantes em {eth_iface}...")
        run_cmd(['ip', 'addr', 'flush', 'dev', eth_iface], check=False)
        
        run_cmd(['ip', 'link', 'set', 'dev', eth_iface, 'up'])
        print(f"[OK] Link up em {eth_iface}.")
        
        run_cmd(['ip', 'addr', 'add', f"{MPC_IP}/{MPC_PREFIX}", 'dev', eth_iface])
        print(f"[OK] Endereço P2P alocado: {MPC_IP}/{MPC_PREFIX}")
        
        for net in MPC_ROUTES:
            run_cmd(['ip', 'route', 'replace', net, 'via', MPC_GW, 'dev', eth_iface, 'onlink'])
            print(f"[OK] Rota agregada: {net} GW {MPC_GW}")
            
        print("\n[INFO] Auditando ICMP ao gateway MPC...")
        res = run_cmd(['ping', '-c', '3', '-W', '2', MPC_GW], check=False)
        if res.returncode == 0:
            print(f"[OK] GW remoto ({MPC_GW}) acessível na malha.")
        else:
            print(f"[AVISO] O gateway de contingência {MPC_GW} não respondeu ICMP. Falta de cabeamento físico?")
            
    except Exception as e:
        print(f"[ERRO] Fluxo operacional falhou com erro sintático/código: {e}")
