# Arquitetura de Dados

## Visão geral

O projeto utiliza uma arquitetura em camadas para preservar os dados
originais, garantir rastreabilidade, aplicar regras de qualidade e
disponibilizar informações analíticas para consumo no Power BI e em
modelos de Machine Learning.

O fluxo foi planejado para suportar carga histórica, processamento
incremental semanal, reprocessamento e auditoria.

```mermaid
flowchart LR
    A[ANP] --> B[Ingestão Python]

    B --> C[RAW<br/>Arquivo original]
    B --> D[Banco de Controle<br/>PostgreSQL]

    C --> E[Fabric Data Factory]

    E --> F[Bronze<br/>Lakehouse]

    F --> G[Data Quality]

    G --> H[Silver<br/>Dados aprovados]
    G --> I[Quarentena<br/>Dados rejeitados]

    H --> J[Gold<br/>Modelo analítico]

    J --> K[Power BI]
    J --> L[Machine Learning]
    S