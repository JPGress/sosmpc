from core.config import C
from core.logger import log
import os
import glob
from datetime import datetime
from core.net_utils import check_root, run_cmd, detect_eth

METADATA = {
    "name": "Restaurar Rollback de Rede (Backup Ethernet)",
    "description": "Lê os temporários gerados na operação de Setup e reconstrói o stack.",
    "active": True
}

def run():
    print(f'\n{C.BOLD}--- {METADATA[\"name\"]} ---{C.RESET}')
    if not check_root():
        log.error("Elevação necessária para manipulação de placa física.")
        return
        
    try:
        eth_iface = detect_eth()
        backups = glob.glob(f"/tmp/eth_backup_{eth_iface}_*.conf")
        if not backups:
            log.warning(f"Histórico nulo para a placa identificada ({eth_iface}). Nenhum BKP criado.")
            return
            
        backups.sort()
        print("\nBackups gravados pelo sistema e detectáveis:")
        for idx, bkp in enumerate(backups, 1):
            ts_str = bkp.split('_')[-1].replace('.conf', '')
            try:
                date_str = datetime.fromtimestamp(int(ts_str)).strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_str = "Timestamp Unrecognized"
            print(f"  {idx}) {os.path.basename(bkp)} [ {date_str} ]")
            
        choice = input("\nForneça ID Numérico do Snapshot (Ou ENTER para utilizar o Mais Recente): ").strip()
        if not choice:
            choice_idx = len(backups) - 1
        elif choice.isdigit() and 1 <= int(choice) <= len(backups):
            choice_idx = int(choice) - 1
        else:
            log.error("Indexamento inválido. Rollback rejeitado.")
            return
            
        bkp_file = backups[choice_idx]
        log.info(f"Compilando restauração: {bkp_file}")
        
        run_cmd(['ip', 'addr', 'flush', 'dev', eth_iface], check=False)
        run_cmd(['ip', 'link', 'set', 'dev', eth_iface, 'up'], check=False)
        
        with open(bkp_file, 'r') as f:
            lines = f.readlines()
            
        bkp_ips = ""
        bkp_routes = ""
        for line in lines:
            if line.startswith("IPS="):
                bkp_ips = line.strip().split('=')[1]
            elif line.startswith("ROUTES="):
                bkp_routes = line.strip().split('=')[1]
                
        for ip_addr in bkp_ips.split():
            run_cmd(['ip', 'addr', 'add', ip_addr, 'dev', eth_iface], check=False)
            log.success(f"Link-local revivido e assinado: {ip_addr}")
            
        for route in bkp_routes.split('|'):
            if route:
                run_cmd(['ip', 'route', 'add'] + route.split(), check=False)
                log.success(f"Tabela atualizada com a rota em cache: {route}")
                
        log.success(f"Snapshot de sistema injetado em malha viva.")
    except Exception as e:
        log.error(f"Stack Trace Failure: {e}")
