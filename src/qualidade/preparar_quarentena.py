import pandas as pd


def preparar_quarentena(
    dados,
    id_execucao,
    arquivo_origem,
):
    """
    Preparo os registros rejeitados para auditoria e
    possível reprocessamento posterior.
    """

    # Seleciono somente os registros classificados como quarentena
    quarentena = (
        dados[
            dados["status_qualidade"] == "QUARENTENA"
        ]
        .copy()
    )

    # Registro a execução responsável pelo processamento
    quarentena["id_execucao"] = id_execucao

    # Registro qual arquivo originou cada linha rejeitada
    quarentena["arquivo_origem"] = arquivo_origem

    # Registro o momento do processamento em UTC para manter
    # uma referência de tempo padronizada no pipeline
    quarentena["data_processamento_utc"] = pd.Timestamp.now(
        tz="UTC"
    )

    return quarentena