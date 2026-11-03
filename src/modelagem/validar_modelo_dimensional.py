from pathlib import Path

import pandas as pd

from src.modelagem.criar_modelo_dimensional import criar_modelo_dimensional


def localizar_gold_mais_recente(caminho_projeto):
    """
    Localizo o Parquet mais recente do dataset Gold
    utilizado como origem da modelagem dimensional.
    """

    diretorio_gold = (
        caminho_projeto
        / "dados"
        / "gold"
        / "anp"
        / "resumo_precos_semanais"
    )

    arquivos_gold = list(
        diretorio_gold.rglob("dados.parquet")
    )

    if not arquivos_gold:
        raise FileNotFoundError(
            "Nenhum arquivo Gold foi encontrado."
        )

    return max(
        arquivos_gold,
        key=lambda arquivo: arquivo.stat().st_mtime,
    )


def validar_modelo():
    """
    Crio o modelo dimensional a partir da Gold mais recente
    e verifico integridade entre fato e dimensões.
    """

    caminho_projeto = Path(__file__).resolve().parents[2]

    caminho_gold = localizar_gold_mais_recente(
        caminho_projeto
    )

    dados_gold = pd.read_parquet(
        caminho_gold
    )

    modelo = criar_modelo_dimensional(
        dados_gold
    )

    dim_tempo = modelo["dim_tempo"]
    dim_localidade = modelo["dim_localidade"]
    dim_produto = modelo["dim_produto"]
    dim_bandeira = modelo["dim_bandeira"]
    fato_preco_semanal = modelo["fato_preco_semanal"]

    print("Gold utilizada:")
    print(caminho_gold)

    print()
    print("Quantidade de registros:")
    print("dim_tempo:", len(dim_tempo))
    print("dim_localidade:", len(dim_localidade))
    print("dim_produto:", len(dim_produto))
    print("dim_bandeira:", len(dim_bandeira))
    print("fato_preco_semanal:", len(fato_preco_semanal))

    print()
    print("Chaves nulas na fato:")
    print(
        "id_tempo:",
        fato_preco_semanal["id_tempo"].isna().sum(),
    )
    print(
        "id_localidade:",
        fato_preco_semanal["id_localidade"].isna().sum(),
    )
    print(
        "id_produto:",
        fato_preco_semanal["id_produto"].isna().sum(),
    )
    print(
        "id_bandeira:",
        fato_preco_semanal["id_bandeira"].isna().sum(),
    )

    print()
    print(
        "Total de coletas na fato:",
        fato_preco_semanal["quantidade_coletas"].sum(),
    )

    print(
        "Linhas Gold:",
        len(dados_gold),
    )


if __name__ == "__main__":
    validar_modelo()