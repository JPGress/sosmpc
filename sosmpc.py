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
from core.dispatcher import Dispatcher
from core.logger import log

def main():
    log.info("Sistema S.O.S. MPC Iniciado.")
    # Auto discovery dos plugins
    plugins_registry = load_plugins()
    if not plugins_registry:
        print("Aviso: Nenhum plugin funcional encontrado no diretório 'plugins/'.")
        log.warning("Inicialização abortada. Lista de plugins vazia.")
        sys.exit(1)
        
    render_menu(plugins_registry)
    # Entrega o controle para o loop do Dispatcher
    Dispatcher.run(plugins_registry)

if __name__ == "__main__":
    main()
