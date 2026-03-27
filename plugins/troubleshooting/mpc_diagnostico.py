import subprocess
from core.net_utils import run_cmd, detect_eth, detect_wifi, get_wifi_default_route
from core.config import MPC_GW, URL_PROXMOX, URL_SOC, WAN_TARGETS

METADATA = {
    "name": "Diagnóstico de Conectividade Extenso (WAN/MPC)",
    "description": "Verifica a integridade via traceroute e ICMP ping para a malha interna local e externa (Google/Cloudflare).",
    "active": True
}

# Tratamento para separar hostname limpo das URLs salvas em const defaults
MPC_PROXMOX = URL_PROXMOX.split('//')[1].split(':')[0]
MPC_SOC_IP = URL_SOC.split('//')[1].split(':')[0]

def ping_host(host: str, count: int = 3, timeout: int = 2) -> bool:
    res = run_cmd(['ping', '-c', str(count), '-W', str(timeout), host], check=False)
    return res.returncode == 0

def testar_wan():
    print("\n--- [ VERIFICAÇÃO WAN — ROTEAMENTO ISP ] ---")
    
    wifi_iface = None
    try:
        wifi_iface = detect_wifi()
    except Exception:
        pass
        
    default_gw = get_wifi_default_route(wifi_iface)
    if not default_gw:
        print("[AVISO] Nenhuma rota Default encontrada. Você está sem acesso de saída Internet/Corporativa.")
        return False
        
    print(f"[INFO] ISP Default Gateway => via {default_gw}")
    
    falhas = 0
    for t in WAN_TARGETS:
        print(f"Ping → {t} ... ", end="", flush=True)
        if ping_host(t):
            print("[ ONLINE ]")
        else:
            print("[ FALHA ]")
            falhas += 1
            
    try:
        res = run_cmd(['curl', '-s', '--max-time', '5', 'https://ifconfig.me'], check=False)
        if res.stdout:
            print(f"[INFO] IP Público Detectado p/ Transição NAT: {res.stdout.strip()}")
        else:
            print("[AVISO] Timeout na porta 443 do ifconfig.me. Ausência real de rede externa detectada.")
    except Exception:
        print("[AVISO] Serviço ou pacote Curl faltando para auditoria completa.")
        
    wan_trc = WAN_TARGETS[0]
    print(f"\n[INFO] Aplicando Traceroute Externo na Host L3 -> {wan_trc}")
    try:
        res = run_cmd(['traceroute', '-n', '-m', '10', '-w', '2', wan_trc], check=False)
        print(res.stdout.strip() if res.stdout else "   [ERRO] ICMP TTL Time-Exceeded sendo bloqueado pelo provider.")
    except Exception:
        print("   [INFO] Instale o pacote 'traceroute' para debug avançado.")
        
    if falhas == 0:
        print("\n[OK] Saída Global ISP sem injúrias na camada TCP/IP.")
    else:
        print(f"\n[ERRO] Redundância externa parcial/offline. ({falhas}/{len(WAN_TARGETS)} alvos inativos).")
    return True

def testar_mpc():
    print("\n--- [ VERIFICAÇÃO OOB DIRETA — RECURSOS DO CLUSTER MPC ] ---")
    
    try:
        eth_iface = detect_eth()
        res = run_cmd(['ip', '-4', 'addr', 'show', 'dev', eth_iface], check=False)
        if 'inet ' not in res.stdout:
            print(f"[ALERTA] Servidor não alocou Virtual IP na placa física ({eth_iface}). Inicie o Setup de Dual NIC.")
    except Exception:
        print("[ERRO] Ethernet ausente fisicamente.")
        
    hosts_core = [
        ("pfSense (GW P2P)", MPC_GW),
        ("Hypervisor Cluster (Proxmox)", MPC_PROXMOX),
        ("DLP Network System (S. Onion)", MPC_SOC_IP)
    ]
    
    falhas = 0
    for l_nome, l_ip in hosts_core:
        print(f"Buscando L3 → {l_nome} ({l_ip}) ... ", end="", flush=True)
        if ping_host(l_ip):
            print("[ ON ]")
        else:
            print("[ TIMEOUT ]")
            falhas += 1
            
    print(f"\n[INFO] Traceroute ao Ponto Leste -> Gateway ({MPC_GW})")
    try:
        res = run_cmd(['traceroute', '-n', '-m', '5', '-w', '2', MPC_GW], check=False)
        print(res.stdout.strip())
    except Exception:
        pass
        
    if ping_host(MPC_GW, count=1, timeout=1):
        print(f"\n[INFO] Traceroute de Switch L2 -> Node Principal ({MPC_PROXMOX})")
        res2 = run_cmd(['traceroute', '-n', '-m', '5', '-w', '2', MPC_PROXMOX], check=False)
        print(res2.stdout.strip())
    else:
        print("\n[AVISO] Traceroute ao nó virtual abortado devido ao salto L2/Gateway estar quebrado.")
        
    if falhas == 0:
        print("\n[OK] Diagnóstico MPC Air-Gapped perfeitamente comunicável.")
    else:
        print(f"\n[FALHA] Integridade deficiente localmente. Nós inalcançáveis: {falhas}")

def run():
    print(f"\n{'='*70}")
    print(f"{METADATA['name']}")
    print(f"{'='*70}")
    
    testar_wan()
    testar_mpc()
    print("\nExecução finalizada.")
