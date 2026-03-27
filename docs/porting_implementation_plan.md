# Portabilidade: Bash para Python (S.O.S. MPC)

## Objetivo
O objetivo deste documento é planejar a portabilidade e "refatoração" do script legado `auto_config_acesso_mpc.sh` (em Bash) para a recém-criada arquitetura em Python (S.O.S. MPC). As opções do script original mapeiam diretamente para funcionalidades ideais a serem separadas em plugins nas áreas de Rede, Troubleshooting e Diversos.

## User Review Required
> [!IMPORTANT]
> Ao lidar com as sub-rotinas do Linux (`ip addr`, `ip route`, etc.), precisaremos de elevação para `root`. Os plugins Python exigirão `os.geteuid() == 0`. Caso o usuário dispare o Menu via usuário comum, os módulos que exigem sudo serão bloqueados emitindo um aviso amigável, sem crashar o menu em si.

> [!WARNING]
> Confirme se o antigo script bash (`auto_config_acesso_mpc.sh` em `00-ORGANIZAR/sh/`) deverá ser removido como parte das tarefas, ou mantido como legado de contingência temporária.

## Proposed Changes

A portabilidade requer a separação das constantes globais, o emprego de um utilitário core em Python e a criação de diversos plugins de acionamento único.

### [Core] Constants & Utilities
- #### [MODIFY] `core/config.py`
  Injeção das constantes do MPC: IPs (`172.16.160.61`), Prefixos, IPs Gateways, Portas (8006, 8080) e URLs de SOC/Proxmox/pfSense.
- #### [NEW] `core/net_utils.py`
  Criação de wrappers comuns em Python que usam a standard library (`subprocess`, `os`) para re-implementar as detecções do bash:
  - `detect_eth(iface_name)`
  - `detect_wifi(iface_name)`
  - `get_wifi_default_route(iface_name)`
  - `require_root()` e `exec_cmd(command)`

### [Plugins] Redes
Foco principal do antigo *auto config*:
- #### [NEW] `plugins/redes/mpc_setup_dual_nic.py`
  Execução completa de configuração Dual-NIC (Backup, Flush, Config, Add Route).
- #### [NEW] `plugins/redes/mpc_flush_eth.py`
  Apenas a restauração/limpeza da porta conectada local `ethX`.
- #### [NEW] `plugins/redes/mpc_rollback_eth.py`
  Leitura dos configs gravados em `/tmp/eth_backup_*` previamentes criados pelo setup, listando à moda iterativa.
- #### [NEW] `plugins/redes/mpc_tunnel_start.py`
  *Fork* do processo SSH no background mantendo o bind na eth0 local/Proxy wlan0.
- #### [NEW] `plugins/redes/mpc_tunnel_stop.py`
  Consulta de PID e término limpo (`kill`) das conexões atreladas ao PID File.

### [Plugins] Troubleshooting
- #### [NEW] `plugins/troubleshooting/mpc_status.py`
  Listagem tabular e colorida com `ip addr show` local de Wi-Fi e Ethernet.
- #### [NEW] `plugins/troubleshooting/mpc_ping_check.py`
  Verificação de `ping -c 3` aos gateways locais e rotas onlink.

### [Plugins] Diversos
- #### [NEW] `plugins/diversos/mpc_portals.py`
  Chama o `xdg-open` disparado para os endereços carregados em `config.py`.

## Verification Plan
1. **Verificação Lógica (`Automated Tests`)**: Utilização do comando pipe (`echo N | python3 sosmpc.py`) não deve incorrer em travamento do menu e deve ser carregado com o plugin recém listado.
2. **Execução Segura / Safe Run**: Como alguns plugins alteram ativamente a rede (`ip addr / route`), simularemos a invocação pelo código confirmando a checagem de root (deve rejeitar se o `uid` for restrito, exibindo permissão negada).
