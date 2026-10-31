import pandas as pd

def preparar_silver(
        dados,
        id_execucao,
        id_arquivo,
        arquivo_origem,
):
    """
    Preparo somente os registros aprovados para a camada Silver,
    aplicando padronizações técnicas e preservando a linhagem.
    """

    dados_silver = dados[
        dados["status_qualidade"] == "APROVADO"
    ].copy()

    # Na Silver passo a utilizar os identificadores já normalizados
    # pelas regras de qualidade aplicadas anteriormente.
    dados_silver["CNPJ"] = dados_silver["cnpj_normalizado"]
    dados_silver["CEP"] = dados_silver["cep_normalizado"]

    # Padronizo os nomes das colunas para facilitar o uso
    # nas próximas camadas e reduzir dependência do formato da origem.
    dados_silver = dados_silver.rename(
        columns={
            "CNPJ": "cnpj",
            "RAZÃO": "razao_social",
            "FANTASIA": "nome_fantasia",
            "ENDEREÇO": "endereco",
            "NÚMERO": "numero",
            "COMPLEMENTO": "complemento",
            "BAIRRO": "bairro",
            "CEP": "cep",
            "MUNICÍPIO": "municipio",
            "ESTADO": "estado",
            "BANDEIRA": "bandeira",
            "PRODUTO": "produto",
            "UNIDADE DE MEDIDA": "unidade_medida",
            "PREÇO DE REVENDA": "preco_revenda",
            "DATA DA COLETA": "data_coleta",
        }
    )

    # Adiciono metadados técnicos para manter a rastreabilidade
    # entre Silver, execução e arquivo de origem.
    dados_silver["id_execucao"] = id_execucao
    dados_silver["id_arquivo"] = id_arquivo
    dados_silver["arquivo_origem"] = arquivo_origem
    dados_silver["data_processamento_utc"] = pd.Timestamp.now(
        tz="UTC"
    )

    colunas_silver = [
        "cnpj",
        "razao_social",
        "nome_fantasia",
        "endereco",
        "numero",
        "complemento",
        "bairro",
        "cep",
        "municipio",
        "estado",
        "bandeira",
        "produto",
        "unidade_medida",
        "preco_revenda",
        "data_coleta",
        "linha_origem",
        "id_execucao",
        "id_arquivo",
        "arquivo_origem",
        "data_processamento_utc",
    ]

    return dados_silver[colunas_silver]