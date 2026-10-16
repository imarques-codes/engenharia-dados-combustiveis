-- Crio o catálogo de arquivos conhecidos pelo pipeline.
-- Cada conteúdo é identificado de forma única pelo hash SHA-256.
CREATE TABLE IF NOT EXISTS controle_arquivo (
    id_arquivo BIGSERIAL PRIMARY KEY,

    nome_arquivo VARCHAR(255) NOT NULL,
    hash_sha256 CHAR(64) NOT NULL UNIQUE,

    fonte VARCHAR(50) NOT NULL DEFAULT 'ANP',

    tamanho_bytes BIGINT NOT NULL,

    caminho_raw TEXT,

    data_primeiro_registro_utc TIMESTAMPTZ
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT ck_controle_arquivo_tamanho
        CHECK (tamanho_bytes >= 0),

    CONSTRAINT ck_controle_arquivo_hash
        CHECK (hash_sha256 ~ '^[0-9a-f]{64}$')
);


-- Registro cada tentativa de processamento realizada pelo pipeline.
-- O UUID será criado pela aplicação Python para permitir rastreamento
-- da execução entre ingestão, qualidade, quarentena e demais camadas.
CREATE TABLE IF NOT EXISTS controle_execucao (
    id_execucao UUID PRIMARY KEY,

    id_arquivo BIGINT NOT NULL,

    tipo_execucao VARCHAR(30) NOT NULL,

    status_execucao VARCHAR(30) NOT NULL,

    data_inicio_utc TIMESTAMPTZ
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    data_fim_utc TIMESTAMPTZ,

    registros_lidos INTEGER,

    registros_aprovados INTEGER,

    registros_quarentena INTEGER,

    mensagem_erro TEXT,

    CONSTRAINT fk_execucao_arquivo
        FOREIGN KEY (id_arquivo)
        REFERENCES controle_arquivo (id_arquivo),

    CONSTRAINT ck_tipo_execucao
        CHECK (
            tipo_execucao IN (
                'BACKFILL',
                'INCREMENTAL',
                'REPROCESSAMENTO'
            )
        ),

    CONSTRAINT ck_status_execucao
        CHECK (
            status_execucao IN (
                'INICIADA',
                'CONCLUIDA',
                'FALHA',
                'IGNORADA_DUPLICIDADE'
            )
        ),

    CONSTRAINT ck_registros_lidos
        CHECK (
            registros_lidos IS NULL
            OR registros_lidos >= 0
        ),

    CONSTRAINT ck_registros_aprovados
        CHECK (
            registros_aprovados IS NULL
            OR registros_aprovados >= 0
        ),

    CONSTRAINT ck_registros_quarentena
        CHECK (
            registros_quarentena IS NULL
            OR registros_quarentena >= 0
        )
);


-- Crio índices para consultas operacionais frequentes
-- sobre status e histórico de execuções.
CREATE INDEX IF NOT EXISTS idx_execucao_status
    ON controle_execucao (status_execucao);


CREATE INDEX IF NOT EXISTS idx_execucao_data_inicio
    ON controle_execucao (data_inicio_utc);