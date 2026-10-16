# Requisitos de Negócio e Dados

## Stakeholders

O projeto considera os seguintes consumidores principais dos dados:

- Inteligência de Mercado
- Pricing
- Business Inteligence
- Ciência de Dados
- Engenharia de Dados

Cada área possui necessidade diferentes, portanto a plataforma deverá disponibilizar dados confiáveis tanto para consumo analítico quanto para precessamento e aplicações de Machine Learning.

## Perguntas de Negócio

### PN-001
Como os preços dos combustíveis evoluem ao longo do tempo?

### PN-002
Quais estados, municípios e regiões apresentam maiores e menores preços?

### PN-003
Qual é a dispersão de preços para o mesmo combustível em diferentes localidades?

### PN-004
Como evolui a relação de preços entre etanol e gasolina?

### PN-005
Quais localidades apresentam maior volatilidade de preços?

### PN-006
Existem valores significativamente diferentes do comportamento regional esperado?

### PN-007
Existe relação entre indicadores externos e a evolução dos preços dos combustíveis?

### PN-008
É possível estimar preços futuros utilizando o histórico e variáveis externas?


## Regras de Negócio Iniciais

### RN-001 — Data de referência
Todo registro utilizado em análises temporais deverá possuir uma data de referência válida.

### RN-002 — Localização
Registros sem localização suficiente não poderão participar de indicadores que dependam desse nível geográfico.

### RN-003 — Preservação
Os dados originais recebidos das fontes deverão ser preservados sem transformação.

### RN-004 — Dados inválidos
Registros considerados inválidos não deverão ser simplesmente descartados.

### RN-005 — Quarentena
Registros rejeitados durante as validações deverão ser armazenados para análise posterior.

### RN-006 — Idempotência
A reexecução do processo de ingestão não deverá criar registros duplicados.

### RN-007 — Rastreabilidade
Todo dado processado deverá possuir informações suficientes para identificar sua origem.

### RN-008 — Auditoria
As execuções dos pipelines deverão registrar status, horário, volume processado e eventuais rejeições.


## Requisitos de Dados

### RD-001 — Histórico
A plataforma deverá permitir carga histórica inicial dos dados disponíveis.

### RD-002 — Carga incremental
Após o backfill inicial, novas execuções deverão priorizar dados novos ou alterados.

### RD-003 — Múltiplas fontes
A arquitetura deverá permitir ingestão proveniente de arquivos, páginas web e APIs.

### RD-004 — Dados brutos
Arquivos e respostas recebidos das fontes deverão ser armazenados antes das transformações.

### RD-005 — Qualidade
Os dados deverão passar por verificações de completude, validade, unicidade e consistência.

### RD-006 — Camada analítica
Os dados tratados deverão ser modelados para consumo analítico e Power BI.

### RD-007 — Machine Learning
A camada analítica deverá permitir a construção futura de conjuntos de dados para treinamento e inferência de modelos.


## Requisitos Não Funcionais

### RNF-001 — Custo
O desenvolvimento deverá priorizar serviços gratuitos, educacionais ou de baixo custo.

### RNF-002 — Segurança
Credenciais, tokens, strings de conexão e segredos não poderão ser armazenados no repositório público.

### RNF-003 — Observabilidade
O pipeline deverá disponibilizar informações suficientes para investigação de falhas.

### RNF-004 — Reprocessamento
Deverá ser possível reprocessar dados históricos a partir dos dados brutos preservados.

### RNF-005 — Escalabilidade
A solução deverá ser capaz de evoluir para volumes maiores sem exigir reconstrução completa da arquitetura.


## Granularidade

A granularidade definitiva será definida após a análise das fontes reais.

A intenção inicial é preservar o maior nível de detalhe disponibilizado pela fonte na camada de ingestão e realizar agregações somente nas camadas analíticas posteriores.


## Periodicidade

A frequência de ingestão será definida de acordo com a frequência real de atualização de cada fonte.

O pipeline não deverá executar cargas desnecessárias apenas para aparentar processamento em tempo real.


## Critérios de Sucesso

O projeto será considerado tecnicamente bem-sucedido quando for possível:

1. ingerir dados automaticamente;
2. preservar os dados originais;
3. identificar dados já processados;
4. impedir duplicações causadas por reprocessamento;
5. registrar problemas de qualidade;
6. recuperar dados rejeitados;
7. transformar dados pelas camadas Bronze, Silver e Gold;
8. disponibilizar modelo analítico para Power BI;
9. integrar variáveis externas;
10. utilizar os dados preparados em um experimento de Machine Learning.