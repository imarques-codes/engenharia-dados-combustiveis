from pathlib import Path


def salvar_modelo_dimensional_local(
    modelo,
    diretorio_modelo,
    id_execucao,
):
    """
    Persisto as dimensões e a tabela fato em arquivos Parquet,
    mantendo um snapshot completo por execução do pipeline.
    """

    diretorio_modelo = Path(
        diretorio_modelo
    )

    diretorio_execucao = (
        diretorio_modelo
        / f"id_execucao={id_execucao}"
    )

    diretorio_execucao.mkdir(
        parents=True,
        exist_ok=True,
    )

    arquivos_salvos = {}

    for nome_tabela, dados in modelo.items():
        caminho_arquivo = (
            diretorio_execucao
            / f"{nome_tabela}.parquet"
        )

        dados.to_parquet(
            caminho_arquivo,
            index=False,
            engine="pyarrow",
        )

        arquivos_salvos[nome_tabela] = caminho_arquivo

        print(
            f"{nome_tabela}: {len(dados)} registros"
        )

    print("Modelo dimensional salvo.")
    print("Caminho:", diretorio_execucao)

    return arquivos_salvos