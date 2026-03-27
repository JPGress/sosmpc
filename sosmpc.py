#!/usr/bin/env python3
import sys
from core.registry import load_plugins
from core.menu import render_menu
from core.dispatcher import dispatch
from core.logger import get_logger

logger = get_logger("main")

def main():
    logger.info("Sistema S.O.S. MPC Iniciado.")
    # Auto discovery dos plugins
    plugins_registry = load_plugins()
    if not plugins_registry:
        print("Aviso: Nenhum plugin funcional encontrado no diretório 'plugins/'.")
        logger.warning("Inicialização abortada. Lista de plugins vazia.")
        sys.exit(1)
        
    running = True
    while running:
        render_menu(plugins_registry)
        try:
            choice = input("Selecione uma opção: ").strip()
            running = dispatch(choice, plugins_registry)
        except KeyboardInterrupt:
            print("\nOperação interrompida pelo usuário de forma abrupta (Ctrl+C).")
            running = False
        except Exception as e:
            logger.error(f"Erro Inesperado no fluxo principal: {e}")
            print(f"\nErro inesperado: {e}")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()
