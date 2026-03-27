import os
from core.net_utils import run_cmd
from core.config import TUNNEL_PID_FILE

METADATA = {
    "name": "Encerrar Tunelamento OOB",
    "description": "Quebra as threads em background rodando o proxy reverso SSH.",
    "active": True
}

def run():
    print(f"\n--- {METADATA['name']} ---")
    if not os.path.isfile(TUNNEL_PID_FILE):
        print(f"[INFO] Nenhum rastro local ({TUNNEL_PID_FILE}). Assumo ausência de threads.")
        return
        
    with open(TUNNEL_PID_FILE, 'r') as f:
        pid = f.read().strip()
        
    if not pid:
        print("[AVISO] PID Track em branco.")
        os.remove(TUNNEL_PID_FILE)
        return
        
    if run_cmd(['kill', '-0', pid], check=False).returncode == 0:
        run_cmd(['kill', pid], check=False)
        print(f"[OK] Fim limpo assinado com OS POSIX via SIGTERM PID {pid}.")
    else:
        print(f"[AVISO] Sombra: Processo {pid} referenciado mas extinto precedentemente.")
        
    os.remove(TUNNEL_PID_FILE)
    print("[OK] Logs temporários removidos do /tmp/")
