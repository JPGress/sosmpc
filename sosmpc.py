#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# sosmpc.py - S.O.S. - Script do Operador de Segurança (MPC)
# ---------------------------------------------------------------------------------
# S.O.S. MPC is an operational security toolkit designed for the 
# Cyber Protection Module (Air-Gapped & Active Defense environments).

from core.config import VERSION, AUTHOR, RELEASE

__version__ = VERSION
__author__ = AUTHOR
__release__ = RELEASE

import sys
from core.registry import load_plugins
from core.menu import render_menu
from core.dispatcher import dispatch
from core.logger import log

def main():
    log.info("Sistema S.O.S. MPC Iniciado.")
    # Auto discovery dos plugins
    plugins_registry = load_plugins()
    if not plugins_registry:
        print("Aviso: Nenhum plugin funcional encontrado no diretório 'plugins/'.")
        log.warning("Inicialização abortada. Lista de plugins vazia.")
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
            log.error(f"Erro Inesperado no fluxo principal: {e}")
            print(f"\nErro inesperado: {e}")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()
