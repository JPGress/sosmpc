# Plano de Refatoração Estética (Clone UX/UI do OwL-PyOpS)

## Objetivo
Clonar as características visuais (layouts, color mappings, error handling format) introduzidas no *owl-PyOpS*, importando a estratégia de gerenciamento de cores da classe `C`, as customizações do log console-mode (`[+]`, `[-]`) e as premissas de formatação do ponto de entrada global, visando "praticamente clonar a estética" no *S.O.S. MPC*.

## Proposed Changes

A manobra exige readequação nuclear das constantes adotadas na fase incipiente do desenvolvimento do *S.O.S. MPC*.

### 1. [MODIFY] `sosmpc.py`
Inclusão do cabeçalho canônico formatado conforme exibido no projeto modelo, declarando atributos da classe *Entrypoint* e removendo as injeções padrão do logger obsoleto que não serão mais utilizadas na camada 0.

### 2. [MODIFY] `core/config.py`
**O paradigma do Dicionário "COLORS" será substituído.**
- Injeção das strings globais: `VERSION`, `RELEASE` e `AUTHOR`.
- Transplante da superclasse `class C:` com dezenas de referências ANSI diretas e otimizadas (`C.BRIGHT_RED`, `C.GRAY`, `C.BG_BLACK`, `C.RED`, `C.BOLD`, etc).
- Criação e portabilidade do design em `ascii_banner()`, formatado sob o espectro Cybervault para invocar graficamente "S.O.S. MPC" e "Script do Operador".

### 3. [MODIFY] `core/logger.py`
Troca completa do handler de módulo *nativo* `logging` pelo decorador customizado *Static Logger* herdado no *owl-PyOpS*. 
Isso permite chamadas elegantes como `log.info()`, `log.error()`, `log.success()`, prefixadas no terminal com marcadores customizados que encantam o usuário visualmente.

### 4. [MODIFY] `core/menu.py` e `core/dispatcher.py`
- Adaptação do `menu.py` para injetar o *banner ASCII* do `config.py` durante o wipe de renderização e tratar o layout hierárquico das chamadas baseadas na tipagem de `C.RES`.
- Reprogramação interna do `dispatcher.py` para apontar às referências de `log` simplificadas (extinguindo dependências do `get_logger`).

### 5. Patch Estrutural Distribuído (Plugins Globais)
Como a arquitetura refatorará o `core/config.py` excluindo a variável legada `COLORS`, os plugins ativos na sub-rotina (`mpc_diagnostico.py`, `mpc_tunnel_start.py`, etc) não subirão caso não migrem da sintaxe em array de *dictionary*. 
Ao invés de reprogramar manualmente os quase 16 submódulos gerados, utilizaremos automação Posix shell iterativo (*sed*) para varrer a árvore `*.py` e renomear dinamicamente os apontamentos:
- `COLORS['green']` torna-se `C.GREEN`
- `COLORS['reset']` torna-se `C.RESET`
- As passagens estritas de importação serão saneadas em Regex.

## Verification Plan
1. Serão disparados os testes brutos de sub-módulo.
2. Aplicativar teste de Interface nula `echo 0 | python3 sosmpc.py` para testemunhar os banners coloridos, identificando imediatamente quebra de imports ou incompatibilidades relativas ao sistema.
