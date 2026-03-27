import subprocess
import time

METADATA = {
    "name": "Identificar Interfaces de Rede",
    "description": "Lista as interfaces de rede do servidor via iproute2.",
    "active": True
}

def run():
    print(f"\n--- {METADATA['name']} ---")
    print("Coletando informações do stack TCP/IP do host...\n")
    time.sleep(0.5)
    try:
        resultado = subprocess.run(['ip', 'a'], capture_output=True, text=True, check=True)
        print(resultado.stdout)
    except FileNotFoundError:
        print("[ERRO] Comando 'ip' não encontrado neste sistema operacional.")
    except Exception as e:
        print(f"[ERRO] Falha ao consultar as interfaces: {e}")
