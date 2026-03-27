import os
import platform
from typing import Dict, Any
from .config import COLORS, GROUP_COLORS

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def render_menu(plugins_registry: Dict[str, Any]):
    clear_screen()
    print(f"{COLORS['bold']}{COLORS['yellow']}=== S.O.S. MPC - Script do Operador de Segurança ==={COLORS['reset']}\n")
    
    # Agrupar plugins para exibiçao
    groups = {}
    for pid, pdata in plugins_registry.items():
        group = pdata.get('group', 'diversos')
        if group not in groups:
            groups[group] = []
        groups[group].append(pdata)
        
    for group, items in groups.items():
        color_name = GROUP_COLORS.get(group, "cyan")
        color_code = COLORS.get(color_name, COLORS["cyan"])
        
        print(f"{color_code}{COLORS['bold']}[ {group.upper()} ]{COLORS['reset']}")
        for item in items:
            status = ""
            if not item.get("active", True):
                status = f" {COLORS['red']}[INATIVO/INSTÁVEL]{COLORS['reset']}"
                
            print(f"  {COLORS['bold']}{item['id']}{COLORS['reset']}. {item['name']}{status}")
        print() 
        
    print(f"{COLORS['red']}{COLORS['bold']}0{COLORS['reset']}. Sair\n")
