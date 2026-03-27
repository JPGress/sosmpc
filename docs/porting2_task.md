# Task List - Refatoração Conectividade

Tarefas para substituir o antigo roteiro bash `teste_conectividade.sh` pela inteligência Python nativa na pasta `troubleshooting/`.

- [x] 1. Alterar `core/config.py` inserindo a constante `WAN_TARGETS` que pauta a detecção de roteamento vivo.
- [x] 2. Apagar os plugins redundantes antigos em `plugins/troubleshooting/` (`mpc_ping_check.py` e `diagnostico.py`).
- [x] 3. Codificar do zero o arquivo `plugins/troubleshooting/mpc_diagnostico.py` abrangendo:
  - Importação do `run_cmd` da biblioteca customizada `net_utils`.
  - Feature 1: Sequência de pings WAN e traceroute com fallback dinâmico.
  - Feature 2: Fetch de IPv4 Público via URL externa segura (`curl`).
  - Feature 3: Varredura dos clusters do MPC (PfSense, Proxmox, SOC).
  - Feature 4: Tabela sintética consolidando alcance e interfaces do Host.
- [x] 4. Rodar automação de entrada nula `echo 0` local para validar registro no UI Registry sem falhas sintáticas de compilação CPython.
