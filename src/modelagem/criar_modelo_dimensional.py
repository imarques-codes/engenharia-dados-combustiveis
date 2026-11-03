import pandas as pd

def criar_modelo_dimensional(dados_gold):
    """
    Transformo a Gold agregada em um modelo dimensional
    composto por dimensões e uma tabela fato.
    """
    dados = dados_gold.copy()

    #Crio a dimensão de produto considerando também a unidade,
    #pois produtos com unidades diferentes não devem ser combinados.
    dim_produto = (
        dados[
            [
                "produto",
                "unidade_medida",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "produto",
                "unidade_medida",
            ]
        )
        .reset_index(drop=True)
    )
    dim_produto["id_produto"] = (
        dim_produto.index + 1
    )

    #Crio a dimensão de localidade a partir de estado e município.
    dim_localidade = (
        dados[
            [
                "estado",
                "municipio",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "estado",
                "municipio",
            ]
        )
        .reset_index(drop=True)
    )

    dim_localidade["id_localidade"] = (
        dim_localidade.index + 1
    )

    #Crio a dimensão de bandeira
    dim_bandeira = (
        dados[
            [
                "bandeira",
            ]
        ]
        .drop_duplicates()
        .sort_values("bandeira")
        .reset_index(drop=True)
    )
    dim_bandeira["id_bandeira"] = (
        dim_bandeira.index + 1
    )

    #Crio a dimensão temporal no nível semanal utilizado pela Gold.
    dim_tempo = (
        dados[
            [
                "ano",
                "semana_iso",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "ano",
                "semana_iso",
            ]
        )
        .reset_index(drop=True)
    )
    dim_tempo["id_tempo"] = (
        dim_tempo.index + 1
    )

    #Substituo os atributos descritivos pelas chaves de dimensões.
    fato_preco_semanal = dados.merge(
        dim_produto,
        on=[
            "produto",
            "unidade_medida",
        ],
        how="left",
    )

    fato_preco_semanal = fato_preco_semanal.merge(
        dim_localidade,
        on=[
            "estado",
            "municipio",
        ],
        how="left",
    )

    fato_preco_semanal = fato_preco_semanal.merge(
        dim_bandeira,
        on="bandeira",
        how="left",
    )

    fato_preco_semanal = fato_preco_semanal.merge(
        dim_tempo,
        on=[
            "ano",
            "semana_iso",
        ],
        how="left",
    )

    colunas_fato = [
        "id_tempo",
        "id_localidade",
        "id_produto",
        "id_bandeira",
        "quantidade_coletas",
        "preco_medio",
        "preco_minimo",
        "preco_maximo",
        "preco_mediano",
        "amplitude_preco",
    ]

    fato_preco_semanal = (
        fato_preco_semanal[colunas_fato].copy()
    )

    return {
        "dim_tempo": dim_tempo,
        "dim_localidade": dim_localidade,
        "dim_produto": dim_produto,
        "dim_bandeira": dim_bandeira,
        "fato_preco_semanal": fato_preco_semanal,
    }