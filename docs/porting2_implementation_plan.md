# Plan: Portabilidade do `teste_conectividade.sh`

## Objetivo
Atender à requisição de portabilidade para Python do script `teste_conectividade.sh`, integrando os diagnósticos (Ping WAN, Curl Pública, Ping MPC e Traceroutes) à interface modular existente do PyOpS (S.O.S. MPC), sem gerar ferramentas sobressalentes desnecessárias.

## Proposed Changes

Atualmente, há na arquitetura os plugins:
- `mpc_ping_check.py`: Cobre um simples `ping` ao gateway do MPC.
- `diagnostico.py`: Um script em estado Placeholder para demonstrar funcionalidades de "inativo/instável".
Para evitarmos redundâncias ("attention to not create unnecessary redundancies"), nossa proposta foca na **substituição** destes módulos básicos por uma suite diagnóstica completa.

### 1. [MODIFY] `core/config.py`
Adição da lista unificada de alvos de teste externos para concentrar a definição no arquivo principal:
- `WAN_TARGETS = ["8.8.8.8", "1.1.1.1", "google.com"]`

### 2. [NEW] Módulo Único de Auditoria
A verificação de conectividade no script bash é sequencial (WAN -> MPC -> Resumo). Separar isso em sub-plugins exigiria múltiplas seleções de menu do usuário. Optou-se por consolidar em um único módulo abrangente de Troubleshooting.
- **`plugins/troubleshooting/mpc_diagnostico.py`**:
  - `testar_wan()`: Disparará sub-shells limitadas rodando Ping, coleta do IPv4 público via Curl em `ifconfig.me` e `traceroute` externo.
  - `testar_mpc()`: Fará ping nos nós constantes no `config.py` (Proxmox, pfSense, Security Onion) e testará alcance interno com `traceroute` para o Gateway.
  - `print_resumo()`: Condensará as inferências no terminal tal qual o script original.

### 3. [DELETE] Remoção de Redundâncias
Os placeholders elaborados nas entregas anteriores que possuem escopo sobreposto serão removidos para entregar um sistema mais limpo (Clean Code):
- **Remover** `plugins/troubleshooting/mpc_ping_check.py` (agora incorporado no diagnóstico completo).
- **Remover** `plugins/troubleshooting/diagnostico.py` (substituído pela versão real).

## Verification Plan
1. **Verificação de Regressões**: Assumimos que a interface modular aceita os subprocessos de `ping` e `traceroute` invocando utilitários nativos em blocos de exceção controlada (Falhas no traceroute por bloqueio não afetam a continuidade do script).
2. O artefato principal de valição será a inicialização limpa usando o atalho `echo 0` para carregar o engine principal.
