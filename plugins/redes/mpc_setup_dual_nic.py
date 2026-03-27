from core.config import C
from core.logger import log
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
        
    log.info(f"Backup salvo temporariamente em: {backup_file}")

def run():
    print(f'\n{C.BOLD}--- {METADATA[\"name\"]} ---{C.RESET}')
    if not check_root():
        log.error("Este módulo altera camadas de roteamento e exige 'sudo'. Acesso negado.")
        return
        
    try:
        eth_iface = detect_eth()
        wifi_iface = detect_wifi()
        wifi_gw = get_wifi_default_route(wifi_iface)
        
        log.info(f"Ethernet : {eth_iface}")
        log.info(f"Wi-Fi    : {wifi_iface or 'N/A'}")
        if wifi_gw:
            log.info(f"Gateway ISP: {wifi_gw}")
            
        backup_eth(eth_iface)
        
        log.info(f"Despejando endereços conflitantes em {eth_iface}...")
        run_cmd(['ip', 'addr', 'flush', 'dev', eth_iface], check=False)
        
        run_cmd(['ip', 'link', 'set', 'dev', eth_iface, 'up'])
        log.success(f"Link up em {eth_iface}.")
        
        run_cmd(['ip', 'addr', 'add', f"{MPC_IP}/{MPC_PREFIX}", 'dev', eth_iface])
        log.success(f"Endereço P2P alocado: {MPC_IP}/{MPC_PREFIX}")
        
        for net in MPC_ROUTES:
            run_cmd(['ip', 'route', 'replace', net, 'via', MPC_GW, 'dev', eth_iface, 'onlink'])
            log.success(f"Rota agregada: {net} GW {MPC_GW}")
            
        log.info(f"Auditando ICMP ao gateway MPC...")
        res = run_cmd(['ping', '-c', '3', '-W', '2', MPC_GW], check=False)
        if res.returncode == 0:
            log.success(f"GW remoto ({MPC_GW}) acessível na malha.")
        else:
            log.warning(f"O gateway de contingência {MPC_GW} não respondeu ICMP. Falta de cabeamento físico?")
            
    except Exception as e:
        log.error(f"Fluxo operacional falhou com erro sintático/código: {e}")
