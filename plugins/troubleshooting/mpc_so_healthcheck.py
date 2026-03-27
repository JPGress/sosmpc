import subprocess
from core.config import C

METADATA = {
    "name": "Healthcheck Remoto SO-Status via SSH",
    "description": "Loga passivamente via SSH no Manager do MPC invocando os hooks so-status, e so-version.",
    "active": True
}

def run():
    print(f"\n{C.BOLD}--- {METADATA['name']} ---{C.RESET}")
    
    ip = input("\nIP/Host do S.O Manager alvo (Ex: 172.16.161.60): ").strip()
    user = input("Usuário da máquina alvo (Sudoer): ").strip()
    
    if not ip or not user:
        return
        
    print(f"\n[INFO] Conectando via shell remota ao TTY. Console nativo irá solicitar chaves/senha do Manager {ip}...")
    
    remote_command = "echo -e '\n=== VERSÃO CONSOLIDADA ==='; sudo so-version; echo -e '\n=== INTEGRIDADE DOCKER SERVICES ==='; sudo so-status"
    cmd = ["ssh", "-t", f"{user}@{ip}", remote_command]
    
    try:
        # PTY Tty handler é mantido ativado pelo '-t' permitindo password prompts do sudo e openssh.
        subprocess.run(cmd)
        print(f"\n{C.GREEN}[OK] Conexão Telemetry desfeita e concluída ao remoto.{C.RESET}")
    except KeyboardInterrupt:
        print("\n[AVISO] Cancelado ativamente pelo Operador durante o trânsito TCP.")
    except Exception as e:
        print(f"{C.RED}[ERRO FATAL] Engine Subprocess perdeu tracking da chave SSH: {e}{C.RESET}")
