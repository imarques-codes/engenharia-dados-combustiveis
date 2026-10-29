from pathlib import Path
import pandas as pd

def salvar_bronze_local(
        dados,
        diretorio_bronze,
        id_execucao,
        id_arquivo,
        arquivo_origem,
        fonte="anp",
):
    """
    Persisto os dados estruturados na camada Bronze
    preservando metadados que permite rastrear sua origem.
    """

    dados_bronze = dados.copy()

    data_ingestao_utc = pd.Timestamp.now(tz="UTC")

    #Adiciono metadados técnicos sem alterar os dados de negócio
    dados_bronze["id_execucao"] = id_execucao
    dados_bronze["id_arquivo"] = id_arquivo
    dados_bronze["arquivo_origem"] = arquivo_origem
    dados_bronze["data_ingestao_utc"] = data_ingestao_utc

    diretorio_bronze = Path(diretorio_bronze)

    caminho_destino = (
        diretorio_bronze
        / fonte.lower()
        / f"ano_ingestao={data_ingestao_utc.year}"
        / f"mes_ingestao={data_ingestao_utc.month:02d}"
        / f"dia_ingestao={data_ingestao_utc.day:02d}"
        / f"id_execucao={id_execucao}"
    )

    caminho_destino.mkdir(
        parents=True,
        exist_ok=True,
    )

    caminho_arquivo = (
        caminho_destino
        / "dados.parquet"
    )
    dados_bronze.to_parquet(
       caminho_arquivo,
       index=False,\
       engine="pyarrow",
    )

    print("Dados salvos na Bronze.")
    print("Registros: ", len(dados_bronze))
    print("Caminho:", caminho_arquivo)

    return caminho_arquivo