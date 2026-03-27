from core.config import C
from core.logger import log
from core.net_utils import check_root, run_cmd, detect_eth
from core.config import MPC_ROUTES, MPC_IP, MPC_PREFIX

METADATA = {
    "name": "Flush de Conexões Ethernet (Limpar)",
    "description": "Zera todos os endereços e blocos de roteamento agregados pelo setup prévio.",
    "active": True
}

def run():
    print(f'\n{C.BOLD}--- {METADATA[\"name\"]} ---{C.RESET}')
    if not check_root():
        log.error("Execução descartada por falta de Sudo (Root Check).")
        return
        
    try:
        eth_iface = detect_eth()
        log.info(f"Resetando link da interface Ethernet ({eth_iface})...")
        
        for net in MPC_ROUTES:
            res = run_cmd(['ip', 'route', 'show', net], check=False)
            if net in res.stdout:
                run_cmd(['ip', 'route', 'del', net], check=False)
                log.success(f"Sub-rota dropada: {net}")
                
        res = run_cmd(['ip', '-4', 'addr', 'show', 'dev', eth_iface], check=False)
        if MPC_IP in res.stdout:
            run_cmd(['ip', 'addr', 'del', f"{MPC_IP}/{MPC_PREFIX}", 'dev', eth_iface], check=False)
            log.success(f"Range de endereçamento cortado do Kernel Space na {eth_iface}")
            
        run_cmd(['ip', 'link', 'set', 'dev', eth_iface, 'down'], check=False)
        log.success(f"NIC local administrativamente desativada.")
        
    except Exception as e:
        log.error(f"Processamento interno falhou: {e}")
