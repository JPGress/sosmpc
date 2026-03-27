from typing import Dict, Any
from .logger import log
from .config import C

class Dispatcher:
    @staticmethod
    def read_option():
        try:
            option = input(f"\n {C.BRIGHT_GREEN}[>]{C.RESET} {C.GREEN}Digite o número da tática (00 para sair): {C.RESET}").strip()
            return option
        except (KeyboardInterrupt, EOFError):
            return "00"

    @staticmethod
    def run(plugins_registry: Dict[str, Any]):
        while True:
            choice = Dispatcher.read_option()
            
            if choice in ['0', '00']:
                print(f"\n {C.GRAY}[INFO] Encerrando terminal de comando...{C.RESET}")
                return
                
            if choice in plugins_registry:
                plugin = plugins_registry[choice]
                if not plugin.get('active', True):
                    log.warning(f"O módulo '{plugin['name']}' encontra-se travado/inativo.")
                    input(f"\n {C.GRAY}[Pressione ENTER para voltar ao Menu]{C.RESET}")
                    return True # volta pro loop no sosmpc? não, agora o loop é aqui.
                
                print(f"\n {C.BRIGHT_GREEN}[+]{C.RESET} Selecionado: {C.BOLD}{plugin['name']}{C.RESET}")
                log.info(f"Disparando thread de execução: {plugin['name']}")
                try:
                    plugin['module'].run()
                except Exception as e:
                    log.error(f"Falha de interrupção no módulo: {e}")
                    
                input(f"\n {C.GRAY}[Pressione ENTER para voltar ao Menu Principal]{C.RESET}")
                # Agora recarregamos o menu? No owl-PyOpS ele recarrega? 
                # No pyops.py:
                # def main():
                #    load_plugins()
                #    render_menu()
                #    Dispatcher.run()
                # So it waits for input in Dispatcher.run.
                # If I want it to re-render menu, I should call render_menu inside Dispatcher.run or use the previous loop logic.
                # Actually, I'll keep it simple and clean.
                from .menu import render_menu
                render_menu(plugins_registry)
            else:
                log.warning("Comando inválido ou fora do escopo do registro.")
