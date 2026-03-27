# Walkthrough: Estruturação Inicial do Projeto S.O.S. MPC

A estruturação completa e construção inicial do *Script do Operador de Segurança (S.O.S. MPC)* foi concluída com sucesso.

## Resumo das Modificações
O projeto Greenfield foi implementado a partir do zero utilizando uma arquitetura modular (`M-V-C` adaptado) nativa em Python 3.10+, focada num ambiente de sistema de defesa *Air-Gapped* restrito, dispensando a necessidade de dependências não nativas para seu funcionamento (utilizando as APIs nativas do Python para UX e gerenciamento).

### Arquivos e Estruturas Implementadas:
1. **Ponto de Entrada Principal (`sosmpc.py`)**: Orquestrador que junta o motor e levanta a UX.
2. **Motor Core (`core/`)**:
   - `config.py`: Constantes dinâmicas do projeto e mapa completo de renderização de Cores ANSI (*Terminal First* UX).
   - `logger.py`: Estrutura simples de auditoria de execução salvando os logs dentro do diretório `logs/`.
   - `menu.py`: Funções renderizadoras modulares exclusivas da camada visual (View), cuidando das demarcações para módulos desabilitados.
   -  `registry.py`: Abstração complexa de Auto-Discovery de plugins, garantindo que adicionar uma funcionalidade futura não requeira modificações na estrutura de menu.
   - `dispatcher.py`: Controler que intercepta e valida os Requests do SysAd e inicia o Modulo destino.
3. **Módulos Práticos (`plugins/`)**:
   - `guias/guia_update.py`: Demonstração operacional estática baseada no update do Módulo MPC via USB.
   - `redes/info_interfaces.py`: Demonstração dinâmica requisitando dados do Sistema Operacional nativamente via `subprocess`.
   - `diversos/utilitario.py`: Exemplo de plugin genérico utilitário.
   - `troubleshooting/diagnostico.py`: Um plugin de rede inicialmente intocado (`active: False`) apenas para provar a feature visual e de defesa de integridade do registro (o menu avisa o bloqueio a testes com instabilidades e impede sua execução).

### Validação
- O sistema MVP foi levantado via execução de testes (`python3 sosmpc.py`). 
- Menus agruparam-se conforme esperado, renderizaram devidamente seus ANSI Colors nativos e processaram sem *crashes* opções e encerramento, garantindo o ciclo da POC.

## Como Executar
Basta entrar no diretório e fazer a chamada local para usufruir e adicionar os próximos plugins da sua necessidade:
```bash
cd /home/r3v4n/Documentos/CyberVault/20_PROJECTS/24_PROFISSIONAL/STI/SOS_MPC/
python3 sosmpc.py
```

## Nova Feature: Portabilidade do `auto_config_acesso_mpc.sh`
O antigo script em Bash isolado em `00-ORGANIZAR/sh/` foi devidamente mapeado, dividido e acoplado na arquitetura nativa Python do *SOS MPC*. Não é mais necessária a execução em shell script solto. Para gerenciar os acessos, a biblioteca `core/net_utils.py` foi criada para operar a stack do `iproute2` sem falhas e sem uso de pacotes pip externos (`subprocess` puro).

### Mapeamento dos Novos Plugins
- **Redes (Setup & Conectividade)**: `mpc_setup_dual_nic.py` (Setup roteado Dual-NIC em Python), `mpc_flush_eth.py` (Limpeza de links), `mpc_rollback_eth.py` (Restauração baseada nas cópias seguras salvas em `/tmp/eth_backup*`).
- **Redes (OOB Lateral Tunnels)**: `mpc_tunnel_start.py` (Conexão SSH em processo isolado / Background) e `mpc_tunnel_stop.py` (Mata o PID do túnel ativo).
- **Troubleshooting**: `mpc_status.py` (Mostra IPs e Rotas para Ethernet e Wi-Fi simultaneamente), `mpc_ping_check.py` (Teste ICMP no Gateway Core).
- **Diversos**: `mpc_portals.py` (Realiza chamadas via `xdg-open` contornando interrupções visuais associadas à janela root/sudo no Linux).

**Segurança**: Todas as chamadas dos plugins de rede possuem detecções de EUID/Superusuário, abortando com o aviso amigável sem apresentar rastros e quebras de Menu (Crash / Traceback) ao usuário caso ele o execute como conta comum.

## Nova Feature: Escalabilidade Diagnóstica (`teste_conectividade.sh`)
Obedecendo ao princípio de evitar "redundâncias desnecessárias" (DRY), o antigo bash de testes em massa foi condensado em único módulo central de rastreio, limpando o código.

- `plugins/troubleshooting/mpc_diagnostico.py`: Substituiu cabalmente os antigos `diagnostico.py` (placeholder) e `mpc_ping_check.py` reduzindo a sobrecarga na leitura do Menu de Interface. O plugin unifica pings de WAN (Google, DNS) usando `subprocess`, extração de IP Público com `curl ifconfig.me`, e traceroutes iterativos tanto para o Backbone da internet quanto para o Gateway Core Air-Gapped do MPC (PfSense, Proxmox, SOC).
