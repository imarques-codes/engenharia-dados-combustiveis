# Catálogo de Fontes de Dados

## Fonte FD-001 — ANP: Levantamento de Preços de Combustíveis

### Responsável

Agência Nacional do Petróleo, Gás Natural e Biocombustíveis — ANP.

### Finalidade

Fonte principal dos preços de combustíveis utilizados pelo projeto.

### Tipo de origem

Dados públicos disponibilizados em arquivos estruturados e páginas web.

### Estratégias de ingestão

#### Histórico

Os arquivos históricos serão utilizados para realizar o backfill inicial
da plataforma.

Objetivo:

- construir histórico;
- testar processamento em maior volume;
- alimentar análises temporais;
- fornecer dados para Machine Learning.

#### Incremental

A página de publicações semanais será consultada automaticamente para
identificar novos arquivos disponibilizados pela ANP.

O scraper deverá detectar novas semanas e identificar os respectivos
links de download.

### Frequência

Semanal, respeitando a frequência de publicação da fonte.

### Granularidade desejada

Preço observado por posto revendedor, produto, localidade e período
de referência, de acordo com a granularidade efetivamente
disponibilizada pela fonte.

### Formatos encontrados

- HTML para descoberta das publicações;
- XLSX para publicações semanais;
- CSV/ZIP para série histórica.

### Tratamento inicial

Os arquivos recebidos não deverão ser alterados antes de sua
persistência na camada RAW.

### Rastreabilidade

Cada arquivo deverá possuir metadados como:

- URL de origem;
- nome do arquivo;
- data e hora de coleta;
- período de referência;
- hash do arquivo;
- tamanho;
- status da ingestão;
- identificador da execução.

### Estratégia de duplicidade

Antes do processamento, o pipeline deverá verificar se o arquivo
ou período já foi ingerido.

A estratégia definitiva utilizará metadados e hash para garantir
idempotência.