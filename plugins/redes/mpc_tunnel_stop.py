from core.config import C
from core.logger import log
import os
from core.net_utils import run_cmd
from core.config import TUNNEL_PID_FILE

METADATA = {
    "name": "Encerrar Tunelamento OOB",
    "description": "Quebra as threads em background rodando o proxy reverso SSH.",
    "active": True
}

def run():
    print(f'\n{C.BOLD}--- {METADATA[\"name\"]} ---{C.RESET}')
    if not os.path.isfile(TUNNEL_PID_FILE):
        log.info(f"Nenhum rastro local ({TUNNEL_PID_FILE}). Assumo ausência de threads.")
        return
        
    with open(TUNNEL_PID_FILE, 'r') as f:
        pid = f.read().strip()
        
    if not pid:
        log.warning("PID Track em branco.")
        os.remove(TUNNEL_PID_FILE)
        return
        
    if run_cmd(['kill', '-0', pid], check=False).returncode == 0:
        run_cmd(['kill', pid], check=False)
        log.success(f"Fim limpo assinado com OS POSIX via SIGTERM PID {pid}.")
    else:
        log.warning(f"Sombra: Processo {pid} referenciado mas extinto precedentemente.")
        
    os.remove(TUNNEL_PID_FILE)
    log.success("Logs temporários removidos do /tmp/")
