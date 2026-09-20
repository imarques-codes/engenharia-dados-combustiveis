# Regras de Qualidade dos Dados

As regras abaixo foram definidas a partir do profiling realizado sobre
os dados reais do Levantamento de Preços de Combustíveis da ANP.

## RQ-001 — Campos críticos

Os seguintes campos são considerados críticos para processamento:

- CNPJ
- RAZÃO
- ENDEREÇO
- MUNICÍPIO
- ESTADO
- PRODUTO
- UNIDADE DE MEDIDA
- PREÇO DE REVENDA
- DATA DA COLETA

Registros com ausência em campos críticos deverão ser analisados e,
quando necessário, direcionados para quarentena.

---

## RQ-002 — Campos opcionais

Os campos abaixo podem possuir valores ausentes sem que o registro
seja automaticamente considerado inválido:

- FANTASIA
- COMPLEMENTO
- BAIRRO

A ausência desses valores deverá ser preservada como informação
desconhecida ou não aplicável.

---

## RQ-003 — CNPJ

O CNPJ será tratado como identificador textual.

Após a normalização, o valor deverá possuir 14 dígitos.

Valores provenientes da fonte com menos de 14 dígitos deverão ser
investigados quanto à possível perda de zeros à esquerda.

A validação futura deverá considerar também os dígitos verificadores.

---

## RQ-004 — CEP

O CEP será tratado como identificador textual.

Após a normalização, o valor esperado deverá possuir 8 dígitos.

Valores fora desse padrão deverão ser identificados para análise.

---

## RQ-005 — Preço de revenda

O preço de revenda deverá possuir valor numérico válido e maior que zero.

Análises de valores extremos deverão considerar o produto e sua unidade
de medida, evitando comparações entre grandezas incompatíveis.

---

## RQ-006 — Produto e unidade de medida

Cada produto deverá possuir unidade de medida compatível.

Na amostra analisada foram encontradas as seguintes relações:

- DIESEL S10 → R$ / litro
- DIESEL S500 → R$ / litro
- ETANOL → R$ / litro
- GASOLINA ADITIVADA → R$ / litro
- GASOLINA COMUM → R$ / litro
- GLP → R$ / 13 kg
- GNV → R$ / m³

Combinações diferentes deverão ser identificadas para investigação.

---

## RQ-007 — Data da coleta

A data da coleta deverá estar dentro do período de referência informado
no arquivo de origem.

Registros fora do período deverão ser direcionados para investigação.

---

## RQ-008 — Duplicidade

Linhas completamente idênticas deverão ser identificadas.

Também deverá ser avaliada a existência de duplicidade segundo uma
chave de negócio.

A chave de negócio definitiva ainda será determinada após análise das
combinações de CNPJ, produto e data da coleta.

---

## RQ-009 — Preservação do dado original

Nenhuma correção deverá sobrescrever o valor recebido originalmente.

Os valores brutos deverão permanecer disponíveis para auditoria,
rastreabilidade e eventual reprocessamento.

## RQ-010 — Chave de negócio candidata

Na amostra semanal analisada, a combinação:

- CNPJ
- PRODUTO
- DATA DA COLETA

não apresentou repetições entre os 19.516 registros.

A combinação será tratada como chave de negócio candidata e deverá
ser revalidada durante o processamento da série histórica antes de
ser considerada definitiva.