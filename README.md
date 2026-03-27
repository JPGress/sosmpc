# S.O.S. MPC - Script do Operador de Segurança (BETA)

```text
        __|    _ \     __|       \  |   _ \    __| 
      \__ \   (   |  \__ \      |\/ |   __/   (    
      ____/  \___/   ____/     _|  _|  _|    \___| 
```

**Versão:** 0.01.000  
**Release:** BETA  
---

## ⚡ Visão Geral

O **S.O.S. MPC** é um toolkit operacional de segurança desenvolvido em **Python 3.10+** (Standard Library Only), projetado especificamente para o **Módulo de Proteção Cibernética (MPC)**. Ele atua como uma camada de prontidão tática que precede a operação formal das ferramentas de defesa ativa (como Security Onion, Suricata e Zeek), garantindo que o hardware e os enlaces de rede estejam íntegros.

O script foi concebido sob a filosofia *Air-Gapped First*, eliminando qualquer dependência de gerenciadores de pacotes externos (`pip`, `apt`) durante a execução, permitindo o uso em servidores isolados e zonas de alta restrição.

---

## ⚙️ Principais Funcionalidades

### 🌐 Conectividade e Redes

- **Dual-NIC Provisioning**: Configuração automatizada de interfaces Ethernet para acesso ao MPC, preservando a rota default de gerenciamento (Wi-Fi/Corporativo).

- **Network Discovery**: Identificação amigável de interfaces físicas, status (UP/DOWN), MAC e endereçamento IP IPv4.

- **OOB Transfer**: Servidor Web embutido para transferência Out-of-Band de arquivos, logs e patches de segurança entre máquinas da malha.

### 🛡️ Manutenção e Segurança

- **Remote Healthcheck**: Consulta via SSH o status do Security Onion (`so-status`) e versões de pacotes sem a necessidade de login manual iterativo.

- **SaltStack Hotfix**: Aplicação remota de patches de autenticação (Bug 2.4.210) para sincronismo de sensores offline.
- **Snapshot Management**: Guia operacional para gestão de estados persistentes via Proxmox VE.

### 🔍 Diagnóstico Avançado

- **Tática de Troubleshooting**: Roteiro de testes ICMP e Traceroute para validar o enlace entre o Gateway L3, Hypervisor L2 e os Nodes Virtuais.

- **Integridade Criptográfica**: Validador SHA256 para checagem de mídias de instalação (ISOs) antes da injeção no ambiente isolado.

---

## 🏗️ Arquitetura do Sistema

O projeto utiliza um design **Modular e Extensível** inspirado no framework *owl-PyOpS*:

- **`sosmpc.py`**: Ponto de entrada (Entrypoint). Realiza verificações de EUID (Root Check) e inicializa o despachante de comandos.
- **`core/`**: O "coração" do sistema.
  - `config.py`: Variáveis de ambiente, constantes de rede (IPs dos nós) e paleta ANSI.
  - `logger.py`: Implementação de log tático visual (`[+]`, `[-]`, `[*]`).
  - `registry.py`: Motor de *Auto-Discovery* que registra plugins dinamicamente.
  - `menu.py`: Renderizador de interface CLI de alta legibilidade.
- **`plugins/`**: Onde as funcionalidades residem.
  - Subpastas: `redes`, `guias`, `troubleshooting`, `diversos`.

---

## 🚀 Requisitos e Uso

### Requisitos Mínimos

- **Python 3.10** ou superior.
- **Linux** (Debian 11+ Homologado).
- **Privilégios**: Execução obrigatória como `root` ou via `sudo`.

### Como Executar

```bash
# 1. Navegue até o diretório do projeto
cd /caminho/para/SOS_MPC

# 2. Execute o toolkit com privilégios administrativos
sudo python3 sosmpc.py
```

---

## 🛠️ Contribuição (Novos Módulos)

Para expandir as capacidades do S.O.S. MPC, basta criar um novo arquivo `.py` em uma das subpastas de `plugins/`. O sistema reconhecerá automaticamente o novo módulo se ele contiver:

```python
METADATA = {
    "name": "Nome da Ferramenta",
    "description": "O que ela faz...",
    "active": True
}

def run():
    # Sua lógica operacional aqui
    pass
```

---
