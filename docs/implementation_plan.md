# Projeto S.O.S. MPC - Script do Operador de Segurança

O objetivo principal desta etapa é estruturar o projeto "S.O.S. MPC" (Script do Operador de Segurança - Módulo de Proteção Cibernética). O script funcionará como uma ferramenta de automação e troubleshooting para os operadores, seguindo uma arquitetura modular similar à do projeto PyOpS. O sistema será baseado em Python 3.10+, sendo terminal-first, com suporte a cores ANSI nativos e sem a necessidade de bibliotecas externas complexas de dependências de interface.

## Riscos da Refatoração / Nova Estruturação

- **Risco de Dependências**: Scripts em Python que possivelmente rodam comandos de sistema em um ambiente *Air-Gapped* podem falhar caso dependam de pacotes não instalados no Debian 11 padrão (sistemas offline). A arquitetura deve focar na biblioteca nativa (Standard Library).
- **Risco de Permissões**: Algumas tarefas de operação e troubleshooting em redes no Linux exigem privilégios elevados (`sudo`). Se executado via usuário comum sem a devida tratativa, instabilidades podem ocorrer.
- **Transição de ferramentas Legadas**: Caso existam scripts antigos em bash sendo "refatorados" p/ Python, pode haver resultados não mapeados devido a diferenças no tratamento de STDOUT/STDERR, além de comportamentos peculiares do binário Linux.

## Estratégia de Rollback (Rollback Strategy)

Como o diretório atual do projeto está vazio (contendo apenas `objetivo_sosmpc.md`), a estratégia de rollback inicial consistirá em:
1. **Controle de Versão (Git)**: Um repositório Git local será utilizado (se desejado). Todos os commits serão controlados. Em caso de falha de projeto ou aprovação recusada perante a nova estrutura estrutural, podemos executar comandos como `git reset --hard` para restaurar o estado limpo.
2. **Remoção de Arquivos do Greenfield**: Em cenários críticos (ou se o Git não estiver em uso ainda no diretório), a exclusão física dos subdiretórios recém-criados (`core/`, `plugins/`, `sosmpc.py` etc.) retornarão o diretório ao seu estado original (vazio) sem causar perdas operacionais em um sistema contínuo.

## Proposed Changes

A estrutura do mock a ser consolidada se espelhará fortemente no modelo testado do `owl-PyOpS` mas adaptado à realidade de infraestrutura/telecom e troubleshooting:

### Core Structure (Módulos Base)
A infraestrutura que sustentará o menu dinâmico, chamadas e registros de ações.
- [NEW] `sosmpc.py`: Ponto de entrada (Entrypoint principal).
- [NEW] `core/__init__.py`: Init module para o pacote principal.
- [NEW] `core/config.py`: Constantes e dicionário de cores ANSI, mantendo UX de terminal.
- [NEW] `core/logger.py`: Estrutura simples para registro de logs e facilitação de debugging em produção.
- [NEW] `core/registry.py`: Lógica para auto-descobrimento (*auto-discovery*) e extração de metadados dinâmicos de plugins. Mapeará itens para o menu de forma transparente.
- [NEW] `core/menu.py`: Renderização de telas separadas logicamente da atuação; lidará visualmente com módulos instáveis / inativos.
- [NEW] `core/dispatcher.py`: Roteador (*Dispatcher*) da entrada do usuário para a ação (plugin) correspondente.

### Plugins (Módulos de Negócio - MVP)
Diretórios que organizarão os plugins operacionais sob a taxonomia requisitada.
- [NEW] `plugins/__init__.py`
- [NEW] `plugins/guias/` e, como base, um script modelo para "Atualização Air-Gapped".
- [NEW] `plugins/redes/` e, como base, um script modelo para "Identificação de Redes / OOB".
- [NEW] `plugins/troubleshooting/` (com um submódulo template base).
- [NEW] `plugins/diversos/` (com um submódulo template base).

### Documentação
- [NEW] `README.md`: Arquivo markdown com as descrições de Objetivo, Requisitos, Instalação, Uso, Contribuição e Licença.

## Verification Plan

### Automated / Syntax Tests
- Executar `python3 sosmpc.py` localmente para garantir o lançamento sem erros de importação e rastrear vazamentos de quebra de arquitetura.
- Testar detecção de erro em módulos problemáticos, atestando que a interface ainda não deve "crashar" o MVP e que eles apareçam marcados como indisponíveis/instáveis no terminal.

### Manual Verification
- Teste visual interativo simulando requisição do usuário (com o agent interagindo limitadamente caso necessário) validando cores ANSI no Output do menu.
- Acesso passo-a-passo às opções categorizadas do MVP visando ver a chamada de tela correspondente aos módulos (Guias, Redes, Troubleshooting, Diversos).
