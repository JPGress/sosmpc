from core.logger import log
from core.config import C
import time

METADATA = {
    "name": "Utilitário Auxiliar Backoffice",
    "description": "Ferramenta para compactar logs rotacionados com mais de 30 dias.",
    "active": True
}

def run():
    print(f'\n{C.BOLD}--- {METADATA[\"name\"]} ---{C.RESET}')
    print("Iniciando varredura no diretório /var/log/mpc/ ... (Mockado)")
    for i in range(1, 4):
        print(f"Compactando pacote {i}...")
        time.sleep(0.3)
    log.info(f"Operação de Limpeza Automática Concluída.")
