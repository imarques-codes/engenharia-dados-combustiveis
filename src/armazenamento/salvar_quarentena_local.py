from pathlib import Path

def salvar_quarentena_local(
        dados,
        diretorio_quarentena,
        id_execucao,
        fonte="anp",
):
    """
    Persisto os registros rejeitados pelas regras de qualidade,
    mantendo os motivos e os metadados necessários para auditoria.
    """
    diretorio_quarentena = Path(
        diretorio_quarentena
    )

    caminho_destino = (
        diretorio_quarentena
        / fonte.lower()
        / f"id_execucao={id_execucao}"
    )

    caminho_destino.mkdir(
        parents=True,
        exist_ok=True,
    )

    caminho_arquivo = (
        caminho_destino
        / "dados_quarentena.parquet"
    )

    dados.to_parquet(
        caminho_arquivo,
        index=False,
        engine="pyarrow",
    )

    print("Dados salvos na Quarentena.")
    print("Registros:", len(dados))
    print("Caminho:", caminho_arquivo)

    return caminho_arquivo