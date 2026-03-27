from core.net_utils import check_root, run_cmd, detect_eth
from core.config import MPC_ROUTES, MPC_IP, MPC_PREFIX

METADATA = {
    "name": "Flush de Conexões Ethernet (Limpar)",
    "description": "Zera todos os endereços e blocos de roteamento agregados pelo setup prévio.",
    "active": True
}

def run():
    print(f"\n--- {METADATA['name']} ---")
    if not check_root():
        print("[ERRO] Execução descartada por falta de Sudo (Root Check).")
        return
        
    try:
        eth_iface = detect_eth()
        print(f"[INFO] Resetando link da interface Ethernet ({eth_iface})...")
        
        for net in MPC_ROUTES:
            res = run_cmd(['ip', 'route', 'show', net], check=False)
            if net in res.stdout:
                run_cmd(['ip', 'route', 'del', net], check=False)
                print(f"[OK] Sub-rota dropada: {net}")
                
        res = run_cmd(['ip', '-4', 'addr', 'show', 'dev', eth_iface], check=False)
        if MPC_IP in res.stdout:
            run_cmd(['ip', 'addr', 'del', f"{MPC_IP}/{MPC_PREFIX}", 'dev', eth_iface], check=False)
            print(f"[OK] Range de endereçamento cortado do Kernel Space na {eth_iface}")
            
        run_cmd(['ip', 'link', 'set', 'dev', eth_iface, 'down'], check=False)
        print(f"[OK] NIC local administrativamente desativada.")
        
    except Exception as e:
        print(f"[ERRO] Processamento interno falhou: {e}")
