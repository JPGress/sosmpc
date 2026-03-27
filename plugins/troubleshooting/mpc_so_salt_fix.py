import subprocess
from core.config import COLORS

METADATA = {
    "name": "Patch Auth Remoto (SaltStack 2.4.210)",
    "description": "Dispara o hotfix de minimum_auth via Bash Injection na máquina afetada off-cluster.",
    "active": True
}

def run():
    print(f"\n{COLORS['bold']}{COLORS['red']}--- {METADATA['name']} ---{COLORS['reset']}")
    print("Módulo de atuação crônica para correção do lock de autenticação 'minimum_auth_version=3'!")
    
    ip = input("\nIP de Roteamento do Nó Isolado (O Sensor ou Search em estado Offline perante o Cluster Manager): ").strip()
    user = input("Nome de usuário atrelado à máquina local quebrada: ").strip()
    
    if not ip or not user:
        return
        
    print(f"\n[AVISO] Injetando rotina agressiva via Wget/Curl sobre a conexão SSH de {ip}.")
    print("O Host subjacente irá requisitar permissões SU.")
    
    script_fix = "curl -fLSs https://raw.githubusercontent.com/Security-Onion-Solutions/securityonion/master/salt/salt/scripts/so-salt-update.sh | sudo bash"
    cmd = ["ssh", "-t", f"{user}@{ip}", script_fix]
    
    try:
        subprocess.run(cmd)
        print(f"\n{COLORS['green']}[OK CONCLUÍDO] Fim da via da inserção do Patch.{COLORS['reset']}")
        print("Tática de Paciência: O Nó precisa compilar no novo min-auth. Volte em 15minutose confirme via 'Healthcheck Remoto'.")
    except Exception as e:
        print(f"{COLORS['red']}[ERRO ROTEAMENTO] SSH sub-thread morta durante sub-processo Curl no endpoint distante: {e}{COLORS['reset']}")
