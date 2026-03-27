import os

# Caminhos absolutos do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(BASE_DIR, 'plugins')

# Configuração Padrão do Terminal (Cores ANSI)
COLORS = {
    "red": "\033[91m",
    "blue": "\033[94m",
    "purple": "\033[95m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "gray": "\033[90m",
    "cyan": "\033[96m",
    "reset": "\033[0m",
    "bold": "\033[1m"
}

# Associação de cores para categorias de módulos no MVP
GROUP_COLORS = {
    "guias": "blue",
    "redes": "purple",
    "troubleshooting": "red",
    "diversos": "gray"
}

# --- CONSTANTES DE REDE E MOVIMENTO LATERAL S.O.S. MPC ---
MPC_IP = "172.16.160.61"
MPC_PREFIX = "24"
MPC_MASK = "255.255.255.0"
MPC_GW = "172.16.160.1"
MPC_DIRECT_NET = "172.16.160.0/24"
MPC_ROUTES = ["172.16.161.0/24"]

URL_PROXMOX = "https://172.16.160.60:8006"
URL_PFSENSE = "http://172.16.160.1"
URL_SOC = "http://172.16.161.60"

TUNNEL_PROXMOX_PORT = "8006"
TUNNEL_PFSENSE_PORT = "8080"
TUNNEL_SOC_PORT = "8161"
TUNNEL_PID_FILE = "/tmp/mpc_ssh_tunnels.pid"
