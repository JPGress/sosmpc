import time

METADATA = {
    "name": "Guia de Atualização (Air-Gapped)",
    "description": "Exibe o passo a passo para atualizar o MPC em ambiente offline homologado.",
    "active": True
}

def run():
    print(f"\n--- {METADATA['name']} ---")
    print(f"{METADATA['description']}\n")
    print("Passo 1: Fazer o download seguro da ISO do binário para a mídia física.")
    print("Passo 2: Inserir a mídia (ex: Pendrive) na porta USB homologada do servidor HPC.")
    print("Passo 3: Executar 'sudo systemctl stop filter-mpc' para interromper o motor.")
    print("Passo 4: Executar o mount e rodar o script instalador 'update.sh'.")
    print("Passo 5: Reiniciar o nó utilizando 'sudo reboot'.")
    time.sleep(0.5)
    print("\n[INFO] Fim do Guia.")
