# Plan: Mecanismos de Atualização Security Onion (S.O.S. MPC)

## Objetivo
Transformar os conhecimentos e procedimentos listados no "Guia de Estratégias Avançadas: Atualização do Security Onion 2.4 em Ambientes Air-Gapped" em módulos interativos para o **S.O.S. MPC**. Lembrando que o script roda na máquina do Operador, englobaremos funcionalidades offline locais (Zona Suja) e execuções remotas conectadas (Zona Limpa via SSH).

## User Review Required
> [!IMPORTANT]
> Como o design proíbe libs instáveis externas (como `paramiko` para SSH), as ações remotas farão chamadas diretas ao binário `ssh/scp` nativo do Linux via `subprocess`. Isso fará com que o terminal peça a senha do *Manager* / *Proxmox* de forma transparente no Console. Isso é plenamente aceitável e mais seguro do que hardcodar credenciais?

## Proposed Changes

Para absorver o manual de forma inteligente, mapeamos os problemas e criamos o seguinte ecossistema de ferramentas modulares:

### 1. [MODIFY] `plugins/guias/guia_update.py`
Aprimoramento do Guia Textual. Atualmente ele faz um "Hello World" de passos. Será atualizado para fornecer no terminal:
- A Matriz de Snapshots do Proxmox.
- O alerta tático de espera de 15 minutos do Salt.
- Dicas do Troubleshooting Avançado para a GUI do Proxmox (Erro 500).

### 2. [NEW] `plugins/diversos/mpc_iso_validator.py`
**Foco:** Pré-Transferência (Zona Suja).
Ferramenta para cálculo nativo em CPython do `sha256sum`. O Operador insere o path da ISO baixada e recebe o laudo bit-a-bit para confrontar com o site oficial da S.O.S. Impede falhas severas de corrupção ou contaminação de binários na ponta.

### 3. [NEW] `plugins/diversos/mpc_remote_backup.py`
**Foco:** Zona Limpa (Enlaçada).
Automação do passo "Backup de Configuração Crítica" sem ter que acessar a GUI. Requisita credenciais temporárias do servidor (apenas para a execução local SSH) e puxa de forma compacta, para o notebook do operador (via `scp`/`ssh -c tar`):
- Proxmox: `/etc/pve`
- Security Onion: `/opt/so/saltstack/local/` e `/opt/so/saltstack/pillar/`
- Salva no path do host: `/tmp/mpc_backups_<timestamp>.tar.gz`

### 4. [NEW] `plugins/troubleshooting/mpc_so_healthcheck.py`
**Foco:** Zona Limpa (Enlaçada).
Verifica a integridade pós-atualização. Atira queries SSH interativas chamando remotamente:
- `sudo so-status`
- `sudo so-version`
- `sudo so-checkin`

### 5. [NEW] `plugins/troubleshooting/mpc_so_salt_fix.py`
**Foco:** Zona Limpa (Enlaçada - Resolutor Crítico).
Destinado à correção manual referenciada (minimum_auth_version 2.4.210). Módulo de um clique em que o operador aponta qual IP de Sensor perdeu conexão após 7 dias, injetando via túnel SSH o `curl -fLSs <patch> | sudo bash`.

## Verification Plan
O pipeline será atestado rodando o menu simulado localmente, testando o carregamento dos painéis ASCII e do parser de módulos, garantindo que o acionamento resulte em erro limpo em ambientes de "mock" nos quais os IPs (172.16.x) não cheguem.
