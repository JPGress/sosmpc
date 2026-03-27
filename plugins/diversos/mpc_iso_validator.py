import os
import hashlib
from core.config import COLORS

METADATA = {
    "name": "Validador Criptográfico Local de ISOs (SHA256)",
    "description": "Realiza checksums de mídias massivas usando a Hashlib nativa antes da Injeção AirGapped.",
    "active": True
}

def run():
    print(f"\n{COLORS['bold']}--- {METADATA['name']} ---{COLORS['reset']}")
    file_path = input("Caminho absoluto ou relativo do arquivo da mídia/ISO: ").strip().strip("'").strip('"')
    
    if not os.path.isfile(file_path):
        print(f"{COLORS['red']}[ERRO] Cadeia de arquivo bloqueada ou Path inacessível à leitura: {file_path}{COLORS['reset']}")
        return
        
    expected_hash = input("Cole a Hash SHA256 Oficial Pública (pular = Vazio): ").strip().lower()
    
    size_mb = os.path.getsize(file_path) / 1024 / 1024
    print(f"\n[INFO] Realizando alocação e stream criptográfico em memória ({size_mb:.2f} MB)... Aguarde.")
    
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                sha256.update(block)
                
        calc_hash = sha256.hexdigest()
        
        print("\n=== Resultado Resumo Lógico ===")
        print(f"Calculado nativamente : {calc_hash}")
        if expected_hash:
            print(f"Assinatura inserida   : {expected_hash}")
        
        if not expected_hash:
            print(f"{COLORS['yellow']}[AVISO] Nenhuma assinatura hash informada como flag. Comportamento analítico puro.{COLORS['reset']}")
        elif calc_hash == expected_hash:
            print(f"{COLORS['green']}[VÁLIDO] A integridade do arquivo binário está perfeitamente alinhada. O Snapshot local é idêntico!{COLORS['reset']}")
        else:
            print(f"{COLORS['red']}[CORRUPTO] CUIDADO ABSOLUTO! O arquivo da MÍDIA não é espelho criptográfico verdadeiro.{COLORS['reset']}")
    except Exception as e:
        print(f"\n[ERRO CRÍTICO] IO read corrompeu na varredura: {e}")
