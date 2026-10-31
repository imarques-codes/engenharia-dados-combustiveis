from pathlib import Path

def salvar_silver_local(
        dados,
        diretorio_silver,
        id_execucao,
        fonte="anp",
):
    """
    Persisto os registros aprovados da camada Silver
    em formato Parquet, particionados por execução.
    """
    diretorio_silver = Path(diretorio_silver)

    caminho_destino = (
        diretorio_silver
        / fonte.lower()
        / f"id_execucao={id_execucao}"
    )

    caminho_destino.mkdir(
        parents=True,
        exist_ok=True,
    )

    caminho_arquivo = (
        caminho_destino/ "dados.parquet"
    )

    dados.to_parquet(
        caminho_arquivo,
        index=False,
        engine="pyarrow",
    )

    print("Dados salvos na Silver")
    print("Registros:", len(dados))
    print("Caminho:", caminho_arquivo)

    return caminho_arquivo