from core.net_utils import run_cmd
from core.config import MPC_GW

METADATA = {
    "name": "Beacon Simples de Ping MPC",
    "description": "Excita a fila local L2 disparando um Ping em linha para o controlador OOB do Cluster.",
    "active": True
}

def run():
    print(f"\n--- {METADATA['name']} ---")
    print(f"[INFO] Processando Echo-Request para IP Gate > {MPC_GW} ...\n")
    
    res = run_cmd(['ping', '-c', '4', '-W', '2', MPC_GW], check=False)
    print("------- STDOUT BUFFER -------")
    print(res.stdout)
    
    if res.returncode == 0:
        print(f"\n[OK] Diagnóstico Perfeito: Enlace transparente e alcançável até {MPC_GW}.")
    else:
        print(f"\n[ERRO] Link inalcançável. Verifique patch cords ou se a subnet isolada foi provisionada no Kernel via Dual-NIC plugin.")
