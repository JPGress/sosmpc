### Guia de Estratégias Avançadas: Atualização do Security Onion 2.4 em Ambientes Air-Gapped via Proxmox VE (Contexto MPC)

##### 1\. Contextualização Estratégica do Módulo de Proteção Cibernética (MPC)

O Módulo de Proteção Cibernética (MPC) é o pilar de sustentação da integridade das redes operacionais nas Organizações Militares de Comunicações. Sua missão primordial é a identificação de invasões e a mitigação de espionagem digital em Nós de Acesso e Centrais Nodais, garantindo que a infraestrutura tática da Força Terrestre permaneça resiliente. Em ambientes de Defesa Nacional, a atualização de sistemas em modo  *air-gapped*  não é apenas uma tarefa de rotina, mas um desafio crítico de logística e segurança.A modernização constante do MPC, operado sobre o hardware Lenovo SE350 (Intel Xeon 8 Cores), visa o robustecimento da capacidade operativa cibernética. O ciclo de atualização mantém a eficácia da defesa baseada em assinaturas e heurísticas, fechando lacunas de detecção (blind spots) que poderiam ser exploradas por adversários. A base para o sucesso dessa operação reside na preparação rigorosa do hipervisor Proxmox VE, que abstrai a complexidade do hardware e fornece as salvaguardas necessárias para intervenções em infraestruturas críticas.

##### 2\. Preparação do Ambiente e Gestão de Mídias (Zona Suja vs. Zona Limpa)

Em operações isoladas, a integridade da mídia é a única barreira contra a corrupção de dados ou a introdução de artefatos maliciosos. O procedimento deve ser dividido entre a  **Zona Suja**  (com acesso à internet) e a  **Zona Limpa**  (ambiente MPC isolado).

###### *Validação na Zona Suja (Pré-transferência)*

**Verificação da Integridade do Arquivo (Checksum SHA256)**

Antes de transferir a mídia de instalação (USB ou DVD) para o ambiente *air-gapped*, é mandatório que o operador valide a integridade do arquivo através da comparação do seu *checksum* SHA256 com o valor oficial fornecido pela Security Onion Solutions. Esta verificação deve ser realizada ainda no ambiente conectado.

| Método de Verificação | Ferramenta | Procedimento |
| :---- | :---- | :---- |
| **Linha de Comando (Linux)** | `sha256sum` | Executar o comando `sha256sum arquivo.iso` e conferir a *hash* gerada bit a bit com a oficial. |
| **Interface Gráfica** | `GtkHash` | Carregar o arquivo ISO na interface, inserir a *hash* oficial no campo "Check" e iniciar a validação. |
| **Confirmação Final** | Integridade de Dados | Assegurar que a *hash* calculada localmente é rigorosamente idêntica à *hash* publicada pela Security Onion Solutions. |

###### *Logística na Zona Limpa (MPC)*

Uma vez validada, a mídia deve ser transportada fisicamente. Recomenda-se o uso de DVD (escrita única) para reduzir riscos de persistência de malware. No MPC, o Security Onion em modo  *airgap*  extrairá os pacotes RPM e regras para o repositório local em /nsm/repo/.

##### 3\. Estratégias de Salvaguarda: Snapshots e Backups no Proxmox VE

Antes de executar a ferramenta soup, o arquiteto deve garantir que a camada de virtualização permita a reversão imediata em caso de kernel panics ou falhas de orquestração.

###### *Pré-requisitos de Armazenamento*

Verifique se o backend de armazenamento do MPC (ZFS ou LVM-Thin no Lenovo SE350) suporta snapshots nativos. O uso de discos em modo RAW sobre LVM tradicional impossibilita snapshots, exigindo clones completos.

###### *Matriz de Decisão de Snapshots*

Tipo de Snapshot,Aplicação,Observação Tática  
Com Memória (Live),Atualizações de containers/Salt,Retorno imediato ao estado de execução.  
Sem Memória (Disk),Atualizações de Kernel/SO,Exige boot fresco; menor ocupação de storage.

###### *Backup de Configuração Crítica*

Snapshots não substituem backups. Extraia e armazene externamente os seguintes diretórios:

* **Proxmox:**  /etc/pve (Configurações do cluster/VMs).  
* **Security Onion:**  /opt/so/saltstack/local/ (Customizações locais) e /opt/so/saltstack/pillar/ (Pilares de configuração).

##### 4\. Execução Técnica: O Procedimento "SOUP" e o Alerta de Versão 2.4.210

O soup (Security Onion UPdater) orquestra o SaltStack e containers Docker sem acesso externo. No ambiente MPC, a precisão na execução é vital.

###### *Fluxo Operacional de Atualização*

1. **Montagem da Mídia:**  Utilize sudo soup \-f /caminho/para/iso.  
2. **Autoupdate do SOUP:**  O script pode identificar uma nova versão de si mesmo. Se solicitado,  **reinicie o comando soup**  imediatamente conforme instrução do terminal.  
3. **Prioridade do Manager:**  O Manager deve ser concluído primeiro. Somente após o destravamento do Salt Master é que os sensores e nós de busca iniciarão seus processos de  *highstate* .\!CAUTION  **ALERTA CRÍTICO DE AUTENTICAÇÃO (SALT 2.4.210)**  A versão 2.4.210 introduz o minimum\_auth\_version \= 3\. Se um sensor ou nó de busca do MPC permanecer offline ou falhar na atualização por mais de  **7 dias**  após o Manager ter sido atualizado, ele será bloqueado pelo Salt Master.  **Correção Manual:**  Caso o nó perca a comunicação, acesse-o via SSH e execute: curl \-fLSs https://raw.githubusercontent.com/Security-Onion-Solutions/securityonion/master/salt/salt/scripts/so-salt-update.sh | sudo bash

##### 5\. Pós-Atualização: Validação de Serviços e Sincronização de Regras

A conclusão do script no Manager é apenas o início da fase de estabilização. Os nós dependem de um check-in aleatório de 15 minutos para processar as mudanças.  
Checklist de Verificação de Integridade

| Comando | Propósito | Resultado Esperado |
| :---- | :---- | :---- |
| `so-status` | Verificar a situação dos contêineres Docker. | Todos devem estar como "Healthy" ou "Running". |
| `so-checkin` | Acionar uma sincronização imediata (`highstate`). | O `highstate` deve ser concluído sem apresentar erros. |
| `so-version` | Confirmar a versão registrada em `/etc/soversion`. | O valor deve coincidir com a versão da ISO empregada. |

###### *Sincronização de Deteção em Modo Airgap*

Em ambientes isolados, as regras são sincronizadas da ISO para caminhos específicos. Falhas de detecção após o update geralmente residem na integridade destes diretórios:

* **Suricata (NIDS):**  /nsm/rules/suricata (Extraído do ET Open na ISO).  
* **Sigma (ElastAlert 2):**  /nsm/repo/rules/sigma (Regras de log).  
* **YARA (Strelka):**  /nsm/rules/yara (Análise de arquivos).

##### 6\. Diagnóstico de Falhas e Troubleshooting Avançado

###### *Erro 500 no Proxmox VE (Integridade da GUI)*

Se a interface web do Proxmox apresentar o erro StdWorkspace.js missing, a causa provável é o uso de scripts de terceiros não autorizados para remoção de avisos de subscrição.

* **Ação:**  É terminantemente proibido o uso de "community scripts" no MPC. A solução é a reinstalação dos pacotes pve-manager e proxmox-widget-toolkit a partir da mídia original verificada.

###### *Falhas de Renderização (Data Failed to Compile)*

Este erro no Salt é frequentemente intermitente. Aguarde a estabilização do boot (até 15 min) e force o check-in: sudo so-checkin

###### *Imagens Docker Ausentes*

Se containers essenciais (Logstash, Elasticsearch, Nginx) não subirem, utilize o refresh do registro local: sudo so-docker-refresh

##### 7\. Considerações Finais e Manutenção de Ciclo de Vida

A resiliência cibernética tática exige disciplina. O MPC é uma plataforma evolutiva; manter o ciclo de atualizações prepara o terreno para a implementação futura de camadas de Inteligência Artificial para análise de anomalias, mitigando ataques  *zero-day*  que escapam às assinaturas tradicionais.**Mandamentos do Administrador MPC Air-Gapped:**

1. **Validarás o Checksum**  na Zona Suja antes de qualquer transferência física.  
2. **Sempre realizarás Snapshots**  e validará o suporte do storage backend (ZFS/LVM-Thin).  
3. **Manager Primeiro, Sempre:**  Nunca force atualizações em sensores sem o nó central íntegro.  
4. **Paciência Tática:**  Respeite a janela de 15 minutos do Salt antes de intervir manualmente.  
5. **Proibirás Scripts Não Autorizados:**  A integridade da GUI do Proxmox é vital para o comando e controle.*Para suporte imediato em campo, utilize a documentação offline integrada disponível no Security Onion Console (SOC).*

