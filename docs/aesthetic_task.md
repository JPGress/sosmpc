# Task List - Refatoração UX / Estética (Clone OwL-PyOpS)

Checklist de modificações nucleares na aplicação S.O.S. MPC visando clonar visualmente e nas tratativas os métodos do repositório *owl-PyOpS*.

- [x] 1. Alterar o cabeçalho base de metadados ("# -*- coding:...") em `sosmpc.py`.
- [x] 2. Destruir `COLORS` no `core/config.py` e importar `VERSION`, `AUTHOR`, `class C:` e o `ascii_banner()`.
- [x] 3. Sobrescrever `core/logger.py` pelo script da classe estática `Logger()` orientada à stdout visual.
- [x] 4. Atualizar `core/dispatcher.py` e `core/menu.py` (Adicionar chamada do *Banner ASCII* e trocar o core do Logger).
- [x] 5. Rodar Automação `find`/`sed` global para varrer a pasta `plugins/` substituindo o parser `COLORS['...']` para `C.COLOR`.
- [x] 6. Rodar automação de teste assíncrono UI nulo (`echo 0`) detectando crash de sintaxes por falta de injeção ANSI.
