from pathlib import Path

def salvar_gold_local(
        dados,
        diretorio_gold,
        id_execucao,
        nome_dataset="resumo_precos_semanais",
        fonte="anp",
):
    """
    Persisto o dataset analítico da camada Gold em formato Parquet,
    mantendo uma organização simples por execução.
    """

    diretorio_gold = Path(
        diretorio_gold
    )

    caminho_destino = (
        diretorio_gold
        /fonte.lower()
        /nome_dataset
        /f"id_execucao={id_execucao}"
    )

    caminho_destino.mkdir(
        parents=True,
        exist_ok=True,
    )

    caminho_arquivo = (
        caminho_destino
        /"dados.parquet"
    )

    dados.to_parquet(
        caminho_arquivo,
        index=False,
        engine="pyarrow",
    )

    print("Dados salvos na Gold.")
    print("Dataset:", nome_dataset)
    print("Registros:", len(dados))
    print("Caminho:", caminho_arquivo)

    return caminho_arquivo