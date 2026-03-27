from typing import Dict, Any
from .logger import get_logger

logger = get_logger(__name__)

def dispatch(choice: str, plugins_registry: Dict[str, Any]) -> bool:
    """Invoca o plugin correspondente se a escolha for válida."""
    if choice == '0':
        print("\nSaindo... Operação encerrada.")
        return False
        
    if choice in plugins_registry:
        plugin = plugins_registry[choice]
        if not plugin.get('active', True):
            print("\nAviso: Este módulo encontra-se inativo ou instável e não pode ser executado no momento.")
            input("\nPressione ENTER para voltar ao menu...")
            return True
            
        print(f"\nIniciando: {plugin['name']}...")
        logger.info(f"Executando ação selecionada: {plugin['name']}")
        try:
            plugin['module'].run()
        except Exception as e:
            logger.error(f"Falha ao rodar o plugin {plugin['name']}: {e}")
            print(f"\n[ERRO] Ocorreu uma falha no módulo: {e}")
            
        input("\nPressione ENTER para voltar ao menu principal...")
    else:
        print("\nOpção inválida.")
        input("Pressione ENTER para tentar novamente...")
        
    return True
