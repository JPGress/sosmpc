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
