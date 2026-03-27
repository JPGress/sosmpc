import os

# Caminhos absolutos do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(BASE_DIR, 'plugins')

VERSION = "0.01.000"
RELEASE = "S.O.S MPC BASE"
AUTHOR = "CyberVault System / Ported from 0wL"

class C:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"

    BG_BLACK="\033[40m"
    BG_RED="\033[41m"
    BG_GREEN="\033[42m"
    BG_YELLOW="\033[43m"
    BG_BLUE="\033[44m"
    BG_MAGENTA="\033[45m"
    BG_CYAN="\033[46m"
    BG_WHITE="\033[47m"
    BG_GRAY="\033[100m"
    BG_BRIGHT_RED="\033[101m"

    BOLD = "\033[1m"
    RESET = "\033[0m"

def ascii_banner():
    return f"""{C.BG_BLACK}{C.CYAN}
       _____     ____     _____         __  __  _____   _____ 
      / ____|   / __ \\   / ____|       |  \\/  ||  __ \\ / ____|
     | (___    | |  | | | (___         | \\  / || |__) | |     
      \\___ \\   | |  | |  \\___ \\        | |\\/| ||  ___/| |     
      ____) |  | |__| |  ____) |       | |  | || |    | |____ 
     |_____/    \\____/  |_____/        |_|  |_||_|     \\_____|
    {C.RESET}"""

GROUP_COLORS = {
    "guias": "BLUE",
    "redes": "MAGENTA",
    "troubleshooting": "RED",
    "diversos": "GRAY"
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

# --- DESTINOS DE AUDITORIA WAN/ISP ---
WAN_TARGETS = ["8.8.8.8", "1.1.1.1", "google.com"]
