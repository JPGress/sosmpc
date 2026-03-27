import os
import platform
from typing import Dict, Any
from .config import C, GROUP_COLORS, ascii_banner, VERSION, AUTHOR, RELEASE


def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def show_header():
    print(ascii_banner())
    print(f"{C.BLACK}      {C.BG_BRIGHT_RED}S.O.S. MPC by {AUTHOR} - v{VERSION} ({RELEASE}) {C.RESET}")
    print(f"{C.RED}+====================================================================================+{C.RESET}")
    print(f"{C.GRAY}       Operador, selecione uma tática informando o número correspondente{C.RESET}")
    print(f"{C.RED}+====================================================================================+{C.RESET}")


def render_menu(plugins_registry: Dict[str, Any]):
    clear_screen()
    show_header()

    # Agrupar plugins para exibiçao
    groups = {}
    for pid, pdata in plugins_registry.items():
        group = pdata.get('group', 'diversos')
        if group not in groups:
            groups[group] = []
        groups[group].append(pdata)

    order = ["guias", "redes", "troubleshooting", "diversos"]

    color_map = {
        "guias": (C.BG_BLUE, C.BLUE),
        "redes": (C.BG_MAGENTA, C.MAGENTA),
        "troubleshooting": (C.BG_RED, C.RED),
        "diversos": (C.BG_WHITE, C.GRAY)
    }

    for group_name in order:
        items = groups.get(group_name, [])
        if not items:
            continue

        bg_color, fg_color = color_map.get(group_name, (C.BG_BLACK, C.CYAN))
        print(f"\n {bg_color}{C.WHITE} [ {group_name.upper()} ] {C.RESET}")

        for item in items:
            status = ""
            if not item.get("active", True):
                status = f" {C.BRIGHT_RED}[INATIVO/INSTÁVEL]{C.RESET}"

            print(
                f"\n {C.BRIGHT_GREEN}[+]{C.RESET}{fg_color} {item['name']}{status}{C.RESET}")
            print(
                f"         {C.GRAY}- {item.get('description', 'S/D')}{C.RESET}")
            print(
                f"         {fg_color}[{item['id']}]{C.RESET} {C.GRAY}Executar{C.RESET}")
            print(f"         {C.GRAY}---{C.RESET}")
        print()

    print(
        f"{C.BRIGHT_RED}{C.BOLD} [0] {C.RESET} {C.GRAY}Encerrar Sessão{C.RESET}\n")
