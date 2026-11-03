import pandas as pd

def preparar_gold_resumo_precos(dados_silver):
    """
    Crio uma visão analítica semanal dos preços de combustíveis
    a partir dos registros aprovados da camada Silver.
    """
    dados = dados_silver.copy()

    dados["data_coleta"] = pd.to_datetime(
        dados["data_coleta"]
    )

    calendario_iso = dados["data_coleta"].dt.isocalendar()

    dados["ano"] = calendario_iso["year"].astype(int)
    dados["semana_iso"] = calendario_iso["week"].astype(int)

    #Agrupo também pela unidade de medida para nunca combinar
    #preços que representam grandeza diferentes

    colunas_agrupamento = [
        "ano",
        "semana_iso",
        "estado",
        "municipio",
        "produto",
        "unidade_medida",
        "bandeira",
    ]

    resumo_precos = (
        dados.groupby(
            colunas_agrupamento,
            dropna=False,
        )
        .agg(
            quantidade_coletas=(
                "preco_revenda",
                "count",
            ),
            preco_medio=(
                "preco_revenda",
                "mean",
            ),
            preco_minimo=(
                "preco_revenda",
                "min",
            ),
            preco_maximo=(
                "preco_revenda",
                "max",
            ),
            preco_mediano=(
                "preco_revenda",
                "median",
            ),
        )
        .reset_index()
    )
    resumo_precos["amplitude_preco"] = (
        resumo_precos["preco_maximo"]
        - resumo_precos["preco_minimo"]
    )
    colunas_precos = [
        "preco_medio",
        "preco_minimo",
        "preco_maximo",
        "preco_mediano",
        "amplitude_preco",
    ]

    resumo_precos[colunas_precos] = (
        resumo_precos[colunas_precos]
        .round(3)
    )
    return resumo_precos