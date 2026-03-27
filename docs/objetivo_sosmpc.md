# Project Rules - Script do Operador de Segurança - S.O.S. MPC

## Objetivo

O objetivo do projeto é criar um script, anterior a operação do MPC, que automatize tarefas repetitivas do operador de segurança e também auxilie em resolução de problemas na operação do Módulo de Proteção Cibernética (MPC), como:

- Identificação das interfaces de Redes;
- Guia de atualização do MPC em ambiente de produção Air-Gapped;
- Configuração de rede para acesso ao MPC;
- Switch de rede para acesso ao MPC;

## Requisitos

- A linguagem de programação deve ser Python 3.10 ou superior.
- O arquivo sosmpc.py deve ser o ponto de entrada do script.
- Estrutura modular, onde cada funcionalidade deve ser um módulo separado.
- Uma vez que o script é executado, ele deve ler os plugins disponíveis no diretório plugins/ e executar cada um deles (Lógica identica ao script pyops.py. Maiores informações da estrutura em "/home/r3v4n/Documentos/CyberVault/20_PROJECTS/23_EDUCACIONAL/234-PORTFOLIO/owl-PyOpS/")
- O script deve ser capaz de ser executado em ambiente Linux (Debian 11 ou superior).
- O script deverá, já em seu MVP, possuir os seguintes módulos:
  - Guias;
  - Redes;
  - Troubleshooting; e
  - Diversos.
- Cada módulo deverá listar as opções disponíveis para o usuário e, ao selecionar uma opção, executar a funcionalidade correspondente.
- Documentações de cada funcionalidade devem estar em formato Markdown e devem ser fáceis de entender.
- O script deverá possuir um arquivo README.md que contenha as seguintes informações:
  - Objetivo do script;
  - Requisitos;
  - Instalação;
  - Uso;
  - Contribuição;
  - Licença;
- Preserve terminal-first UX.
- Keep ANSI color support without forcing external libraries.
- Do not mix menu rendering with operational handlers.
- Every option must map to a registered handler.
- Disabled and unstable options must be visibly marked.
- Prefer modular Python over monolithic files.
- Keep code readable for someone migrating from Bash to Python.
- Avoid unnecessary frameworks.

