import os
import time
import subprocess
from core.config import COLORS

METADATA = {
    "name": "Retirar Backup Remoto SCP de PVE / S.O",
    "description": "Via SSH, comprime e exporta arquivos críticos (/opt/so/pillar e /etc/pve) do nó Air-Gapped para máquina local host.",
    "active": True
}

def run():
    print(f"\n{COLORS['bold']}--- {METADATA['name']} ---{COLORS['reset']}")
    
    target_ip = input("IP Address do Cluster Remoto PVE ou S.O Manager: ").strip()
    target_user = input("Nome de Usuário Linux Remoto (ex: root, admin, ubuntu): ").strip()
    
    if not target_ip or not target_user:
        print(f"{COLORS['yellow']}[AVISO] Informações faltantes para abrir o socket remoto.{COLORS['reset']}")
        return
        
    bkp_dir = f"/tmp/mpc_backups_{int(time.time())}"
    os.makedirs(bkp_dir, exist_ok=True)
    
    print(f"\n[INFO] {COLORS['red']}Segurança:{COLORS['reset']} A porta passiva pedirá credenciais em tela oculta do seu console SSH nativo para {target_ip}.")
    print(f"Salvaremos tudo na diretiva limpa Host -> {bkp_dir}")
    print("\n* Processo Fase 1 (Configurações do Node S.O SaltStack) ...")
    
    # Executamos o scp abrindo o stdin para o usuário, não interceptando IO via pipes.
    try:
        cmd1 = ["scp", "-r", "-O", f"{target_user}@{target_ip}:/opt/so/saltstack/local", bkp_dir]
        subprocess.run(cmd1)
        
        cmd2 = ["scp", "-r", "-O", f"{target_user}@{target_ip}:/opt/so/saltstack/pillar", bkp_dir]
        subprocess.run(cmd2)
        
        print("\n* Processo Fase 2 (Configuração VM/Qemu do Hipervisor Proxmox) ...")
        cmd3 = ["scp", "-r", "-O", f"{target_user}@{target_ip}:/etc/pve", bkp_dir]
        subprocess.run(cmd3)
        
        print(f"\n{COLORS['green']}[OK] Sessões fechadas.{COLORS['reset']}")
        print(f"Os artefatos Lógicos foram mapeados e alvos contidos em => {bkp_dir}.")
    except Exception as e:
        print(f"{COLORS['red']}[ERRO POSIX/SCP] Disparo por Secure Copy Protocol travou: {e}{COLORS['reset']}")
