# Task List - Refatoração do Bash (auto_config_acesso_mpc.sh)

Esta é a lista numerada para a estruturação modular das funcionalidades presentes no bash legado para a Engine do `S.O.S. MPC`.

- [x] 1. Atualizar o `core/config.py` injetando todas as chaves e caminhos (Portas, IPs, URLs) extraídas do Bash script.
- [x] 2. Desenvolver o Módulo Core de Utilidades `core/net_utils.py`, adaptando funções iterativas em bash (`detect_eth`, `detect_wifi`, checagem de perimssão ROOT) para wrappers Python utilizando `subprocess`.
- [x] 3. Criar plugin **Setup Dual-NIC Completo** (`plugins/redes/mpc_setup_dual_nic.py`).
- [x] 4. Criar plugin **Flush de Interface** (`plugins/redes/mpc_flush_eth.py`).
- [x] 5. Criar plugin **Restauração de Arquivos/Rotas** (`plugins/redes/mpc_rollback_eth.py`).
- [x] 6. Criar plugin **Início de Túnel Distribuído SSH** (`plugins/redes/mpc_tunnel_start.py`).
- [x] 7. Criar plugin **Encerramento de Túnel** (`plugins/redes/mpc_tunnel_stop.py`).
- [x] 8. Criar plugin utilitário de leitura em **Troubleshooting**: `plugins/troubleshooting/mpc_status.py`.
- [x] 9. Criar plugin de conectividade em **Troubleshooting**: `plugins/troubleshooting/mpc_ping_check.py`.
- [x] 10. Criar plugin de Portais em **Diversos**: `plugins/diversos/mpc_portals.py`.
- [x] 11. Validação final, assegurando que faltas de dependências de Sudo abortam as ações adequadamente, invés de poluir e quebrar o terminal.
