import os
import subprocess
import glob
from typing import Optional, List
from core.logger import get_logger

logger = get_logger(__name__)

def check_root() -> bool:
    """Verifica se o script está rodando como root."""
    return os.geteuid() == 0

def run_cmd(cmd: List[str], check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    """Wrapper para subprocess.run que loga o processo para fail-safe debug."""
    logger.debug(f"Executando processo sub-shell: {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=text, check=check)

def detect_eth(force_iface: Optional[str] = None) -> str:
    """Retorna a primeira interface com driver Ethernet físico."""
    if force_iface:
        run_cmd(['ip', 'link', 'show', force_iface])
        return force_iface
        
    for iface_path in glob.glob('/sys/class/net/*/'):
        iface = os.path.basename(os.path.dirname(iface_path))
        if iface == 'lo':
            continue
            
        type_path = os.path.join(iface_path, 'type')
        wireless_path = os.path.join(iface_path, 'wireless')
        phy_path = os.path.join(iface_path, 'phy80211')
        
        if os.path.isfile(type_path):
            with open(type_path, 'r') as f:
                iface_type = f.read().strip()
            
            # Type 1 = Ethernet, e sem diretórios identificadores de wireless = wired
            if iface_type == "1" and not os.path.isdir(wireless_path) and not os.path.isdir(phy_path):
                return iface
                
    raise RuntimeError("Nenhuma interface de cabo (Ethernet) encontrada no Host.")

def detect_wifi(force_iface: Optional[str] = None) -> Optional[str]:
    """Retorna a primeira interface Wi-Fi encontrada."""
    if force_iface:
        run_cmd(['ip', 'link', 'show', force_iface])
        return force_iface
        
    for iface_path in glob.glob('/sys/class/net/*/'):
        iface = os.path.basename(os.path.dirname(iface_path))
        wireless_path = os.path.join(iface_path, 'wireless')
        phy_path = os.path.join(iface_path, 'phy80211')
        
        if os.path.isdir(wireless_path) or os.path.isdir(phy_path):
            return iface
            
    return None

def get_wifi_default_route(wifi_iface: Optional[str]) -> Optional[str]:
    """Retorna o IP do gateway default atrelado à interface de rede Wi-Fi."""
    try:
        res = run_cmd(['ip', 'route', 'show', 'default'])
        routes = res.stdout.splitlines()
        
        if not wifi_iface:
            if routes:
                parts = routes[0].split()
                if 'via' in parts:
                    return parts[parts.index('via') + 1]
            return None
            
        for route in routes:
            if f"dev {wifi_iface}" in route:
                parts = route.split()
                if 'via' in parts:
                    return parts[parts.index('via') + 1]
    except Exception as e:
        logger.error(f"Erro ao extrair as rotas iproute via interface wlan {wifi_iface}: {e}")
        
    return None
