import os
import importlib.util
from typing import Dict, Any
from .config import PLUGINS_DIR
from .logger import log

def load_plugins() -> Dict[str, Any]:
    """
    Rastreia o diretório de plugins e os registra.
    Espera-se que cada plugin defina METADATA contendo 'name', 'description', e 'active'.
    O 'group' será inferido a partir do nome da pasta pai (ex: redes, guias).
    """
    registry = {}
    
    if not os.path.exists(PLUGINS_DIR):
        log.warning(f"Diretório de plugins não encontrado: {PLUGINS_DIR}")
        return registry

    plugin_id_counter = 1

    for group_name in os.listdir(PLUGINS_DIR):
        group_path = os.path.join(PLUGINS_DIR, group_name)
        if not os.path.isdir(group_path) or group_name.startswith('__'):
            continue
            
        for file_name in os.listdir(group_path):
            if file_name.endswith('.py') and not file_name.startswith('__'):
                file_path = os.path.join(group_path, file_name)
                module_name = file_name[:-3]
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'METADATA') and hasattr(module, 'run'):
                        plugin_info = module.METADATA.copy()
                        plugin_info['group'] = group_name
                        plugin_info['module'] = module
                        plugin_info['id'] = str(plugin_id_counter)
                        
                        # Garantir estado padrao
                        if 'active' not in plugin_info:
                            plugin_info['active'] = True
                            
                        registry[plugin_info['id']] = plugin_info
                        plugin_id_counter += 1
                        log.info(f"Plugin registrado: {plugin_info['name']} (Grupo: {group_name})")
                    else:
                        log.warning(f"Módulo {file_name} ignorado. Faltam 'METADATA' ou função 'run()'.")
                except Exception as e:
                    log.error(f"Erro ao carregar o plugin {file_path}: {e}")
                    
    return registry
