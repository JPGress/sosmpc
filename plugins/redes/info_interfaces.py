import subprocess
import re
from core.config import C
from core.logger import log

METADATA = {
    "name": "Identificar Interfaces de Rede",
    "description": "Lista as interfaces de rede do servidor via iproute2 de forma amigável.",
    "group": "redes",
    "active": True
}

def run():
    print(f"\n{C.BOLD}--- {METADATA['name']} ---{C.RESET}")
    log.info("Coletando informações das interfaces físicas e virtuais...\n")
    
    try:
        # Usando ip addr show para capturar o estado real
        resultado = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True, check=True)
        raw_output = resultado.stdout
        
        # Split por interface (linhas que começam com número e dois pontos)
        interfaces = re.split(r'^\d+:\s+', raw_output, flags=re.MULTILINE)[1:]

        print(f" {C.WHITE}{C.BG_BLUE} {'INTERFACE':<15} | {'STATUS':<10} | {'IPv4 ADDRESS':<18} | {'MAC ADDRESS':<18} {C.RESET}")
        print(f" {C.GRAY}{'-'*75}{C.RESET}")

        for iface_raw in interfaces:
            lines = iface_raw.splitlines()
            first_line = lines[0]
            
            # extrair nome
            name = first_line.split(':')[0]
            
            # extrair status
            status = "UP" if "UP" in first_line else "DOWN"
            color_status = C.GREEN if status == "UP" else C.RED
            
            # extrair ip
            ip = "N/A"
            for line in lines:
                if "inet " in line:
                    ip = line.split()[1]
                    break
            
            # extrair mac
            mac = "N/A"
            for line in lines:
                if "link/ether" in line:
                    mac = line.split()[1]
                    break

            print(f" {C.BOLD}{name:<15}{C.RESET} | {color_status}{status:<10}{C.RESET} | {C.CYAN}{ip:<18}{C.RESET} | {C.GRAY}{mac:<18}{C.RESET}")

        print(f"\n{C.GRAY}Dica: Utilize 'Configuração MPC' para associar IPs estáticos à interface Ethernet.{C.RESET}")

    except Exception as e:
        log.error(f"Falha ao processar as interfaces: {e}")
