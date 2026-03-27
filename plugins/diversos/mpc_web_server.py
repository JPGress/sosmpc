import http.server
import socketserver
import socket
import os
import subprocess
import re
from core.config import C
from core.logger import log

METADATA = {
    "name": "Servidor Web Transmitente (Transferencia OOB)",
    "description": "Inicia um servidor HTTP estático para transferência de arquivos e logs no ambiente MPC.",
    "group": "diversos",
    "active": True
}

def get_interfaces():
    """Retorna lista de (nome, ip) usando ip addr (Padrão Linux)"""
    interfaces = []
    try:
        resultado = subprocess.run(['ip', '-4', 'addr', 'show'], capture_output=True, text=True, check=True)
        raw_output = resultado.stdout
        # Split por interface
        blocks = re.split(r'^\d+:\s+', raw_output, flags=re.MULTILINE)[1:]
        for block in blocks:
            name = block.split(':')[0]
            ip = "N/A"
            for line in block.splitlines():
                if "inet " in line:
                    ip = line.split()[1].split('/')[0]
                    break
            if ip != "N/A" and ip != "127.0.0.1":
                interfaces.append((name, ip))
    except Exception as e:
        log.error(f"Erro ao detectar interfaces: {e}")
    return interfaces

def run():
    print(f"\n{C.BOLD}--- {METADATA['name']} ---{C.RESET}")
    log.info("Iniciando utilitário de transferência Web...")

    interfaces = get_interfaces()
    if not interfaces:
        log.error("Nenhuma interface de rede IPv4 ativa encontrada para bind.")
        return

    print("\n[ Interfaces Disponíveis para Distribuição ]")
    for i, (name, ip) in enumerate(interfaces):
        print(f"  [{i+1}] {name:<12} -> {C.CYAN}{ip}{C.RESET}")
    print(f"  [0] Cancelar Operação")

    try:
        choice = input(f"\n {C.BRIGHT_GREEN}[>]{C.RESET} Selecione a interface para binding: ").strip()
        if choice == '0' or not choice:
            return
        
        idx = int(choice) - 1
        if not (0 <= idx < len(interfaces)):
            log.warning("Opção inválida.")
            return
        
        selected_ip = interfaces[idx][1]
        
        port_input = input(f" {C.BRIGHT_GREEN}[>]{C.RESET} Informe a porta TCP (Padrão 8000): ").strip()
        port = int(port_input) if port_input else 8000
        
        # Configuração do Handler
        Handler = http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        
        path = os.getcwd()
        log.info(f"Servindo diretório: {C.BOLD}{path}{C.RESET}")
        log.success(f"Servidor ATIVO em: {C.BRIGHT_YELLOW}http://{selected_ip}:{port}/{C.RESET}")
        print(f" {C.GRAY}Aviso: Apenas para uso temporário. Use Ctrl+C para encerrar.{C.RESET}\n")
        
        with socketserver.TCPServer((selected_ip, port), Handler) as httpd:
            httpd.serve_forever()
            
    except ValueError:
        log.error("Entrada inválida. Digite apenas números.")
    except KeyboardInterrupt:
        print("\n")
        log.warning("Servidor encerrado pelo operador.")
    except Exception as e:
        log.error(f"Erro fatal no socket do servidor: {e}")
