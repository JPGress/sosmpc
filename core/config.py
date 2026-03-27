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
