# S.O.S. MPC - Script do Operador de Segurança

## Objetivo

O objetivo deste projeto é criar um script que automatize tarefas repetitivas do operador de segurança e auxilie na resolução de problemas na operação do Módulo de Proteção Cibernética (MPC), rodando antes da operação formal do MPC.

## Requisitos

- Python 3.10 ou superior.
- Sistema Operacional Linux (Debian 11 ou superior homologado).
- Terminal com suporte a cores ANSI.

## Instalação

Sendo um script nativo com standard library, ele é aderente a ambientes *Air-Gapped* e não requer `pip install`.

```bash
# Clone ou copie o diretório:
git clone <URL_DO_REPOSITORIO> sosmpc
cd sosmpc
```

## Uso

O ponto de entrada único é o arquivo `sosmpc.py`.

```bash
python3 sosmpc.py
```

Navegue pelo menu via terminal e escolha as opções apresentadas de acordo.

## Contribuição

O sistema foi construído em arquitetura modular. Para adicionar uma nova funcionalidade, crie um arquivo dentro de `plugins/<categoria>/` (ex: `guias`, `redes`, `troubleshooting` ou `diversos`).
A funcionalidade será automaticamente registrada pelo `core.registry` e exibida no menu.

## Licença

MIT (Ou a política interna de segurança e licença da corporação responsável pelo projeto).
