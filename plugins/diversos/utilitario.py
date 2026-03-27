import time

METADATA = {
    "name": "Utilitário Auxiliar Backoffice",
    "description": "Ferramenta para compactar logs rotacionados com mais de 30 dias.",
    "active": True
}

def run():
    print(f"\n--- {METADATA['name']} ---")
    print("Iniciando varredura no diretório /var/log/mpc/ ... (Mockado)")
    for i in range(1, 4):
        print(f"Compactando pacote {i}...")
        time.sleep(0.3)
    print("\n[INFO] Operação de Limpeza Automática Concluída.")
