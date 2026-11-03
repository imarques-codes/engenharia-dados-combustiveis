import argparse
from pathlib import Path

import pandas as pd

from src.armazenamento.salvar_gold_local import salvar_gold_local
from src.transformacao.preparar_gold import preparar_gold_resumo_precos
from src.armazenamento.salvar_quarentena_local import salvar_quarentena_local
from src.armazenamento.salvar_silver_local import salvar_silver_local
from src.transformacao.preparar_silver import preparar_silver
from src.armazenamento.salvar_bronze_local import salvar_bronze_local
from src.armazenamento.salvar_raw_local import salvar_arquivo_raw
from src.banco.atualizar_caminho_raw import atualizar_caminho_raw
from src.banco.registrar_arquivo import registrar_arquivo
from src.banco.registrar_execucao import (
    concluir_execucao,
    iniciar_execucao,
    registrar_execucao_ignorada,
    registrar_falha,
)
from src.banco.verificar_processamento import arquivo_ja_processado
from src.qualidade.classificar_registro import avaliar_qualidade_registro
from src.qualidade.preparar_quarentena import preparar_quarentena
from src.qualidade.validar_cep import (
    classificar_cep,
    normalizar_cep,
    validar_formato_cep,
)
from src.qualidade.validar_cnpj import (
    normalizar_cnpj,
    validar_cnpj,
)

def obter_argumentos():
    """
    Defino os parâmetros que posso informar pelo terminal
    ao iniciar o pipeline.
    """

    parser = argparse.ArgumentParser(
        description="Executa o pipeline local de dados da ANP"
    )

    parser.add_argument(
        "--arquivo",
        type=Path,
        help="Caminho do arquivo da ANP que será processado.",
    )

    parser.add_argument(
        "--tipo",
        choices=["backfill", "incremental"],
        default="backfill",
        help="Define o tipo da carga. Padrão: backfill.",
    )

    parser.add_argument(
        "--reprocessar",
        action="store_true",
        help="Permite reprocessar um arquivo já concluido.",
    )

    return parser.parse_args()


def carregar_dados_anp(caminho_arquivo):
    """
    Carrego a planilha da ANP definindo explicitamente
    o schema das colunas textuais da fonte.
    """

    colunas_texto = {
        "CNPJ": "string",
        "RAZÃO": "string",
        "FANTASIA": "string",
        "ENDEREÇO": "string",
        "NÚMERO": "string",
        "COMPLEMENTO": "string",
        "BAIRRO": "string",
        "CEP": "string",
        "MUNICÍPIO": "string",
        "ESTADO": "string",
        "BANDEIRA": "string",
        "PRODUTO": "string",
        "UNIDADE DE MEDIDA": "string",
    }

    return pd.read_excel(
        caminho_arquivo,
        sheet_name="POSTOS REVENDEDORES",
        header=9,
        dtype=colunas_texto,
    )


def aplicar_regras_qualidade(dados):
    """
    Aplico as regras de CNPJ e CEP já validadas anteriormente
    e classifico cada registro.
    """

    dados = dados.copy()

    dados["linha_origem"] = dados.index + 11

    dados["cnpj_normalizado"] = (
        dados["CNPJ"].apply(normalizar_cnpj)
    )

    dados["cnpj_valido"] = (
        dados["CNPJ"].apply(validar_cnpj)
    )

    dados["classificacao_cep"] = (
        dados["CEP"].apply(classificar_cep)
    )

    dados["cep_normalizado"] = (
        dados["CEP"].apply(normalizar_cep)
    )

    dados["cep_formato_valido"] = (
        dados["CEP"].apply(validar_formato_cep)
    )

    dados[
        [
            "status_qualidade",
            "motivo_quarentena",
        ]
    ] = dados.apply(
        lambda linha: avaliar_qualidade_registro(
            linha["cnpj_valido"],
            linha["cep_formato_valido"],
        ),
        axis=1,
        result_type="expand",
    )

    return dados


def executar_pipeline(
    caminho_arquivo,
    tipo_execucao="BACKFILL",
    permitir_reprocessamento=False,
):
    """
    Orquestro o processamento local do arquivo desde
    o controle de entrada até o registro das métricas.
    """

    caminho_arquivo = Path(caminho_arquivo)

    id_execucao = None

    try:
        id_arquivo = registrar_arquivo(
            caminho_arquivo
        )

        # Preservo o arquivo original na RAW antes de iniciar
        # qualquer transformação sobre os dados.
        caminho_projeto = Path(__file__).resolve().parents[2]

        diretorio_raw = (
            caminho_projeto
            / "dados"
            / "raw"
        )

        caminho_raw_absoluto = salvar_arquivo_raw(
            caminho_origem=caminho_arquivo,
            diretorio_raw=diretorio_raw,
            fonte="anp",
        )

        # Registro no catálogo um caminho relativo para não depender
        # da estrutura específica deste computador.
        caminho_raw_relativo = caminho_raw_absoluto.relative_to(
            caminho_projeto
        )

        atualizar_caminho_raw(
            id_arquivo=id_arquivo,
            caminho_raw=caminho_raw_relativo,
        )

        # Verifico se este arquivo já possui uma execução concluída.
        ja_processado = arquivo_ja_processado(
            id_arquivo
        )

        if ja_processado and not permitir_reprocessamento:
            id_execucao = registrar_execucao_ignorada(
                id_arquivo=id_arquivo,
                tipo_execucao=tipo_execucao,
            )

            print("Processamento ignorado.")
            print("Motivo: arquivo já processado com sucesso.")
            print("ID da execução:", id_execucao)

            return

        if ja_processado and permitir_reprocessamento:
            tipo_execucao = "REPROCESSAMENTO"

        id_execucao = iniciar_execucao(
            id_arquivo=id_arquivo,
            tipo_execucao=tipo_execucao,
        )

        print("Execução iniciada.")
        print("ID da execução:", id_execucao)

        dados = carregar_dados_anp(
            caminho_arquivo
        )

        # Persisto na Bronze os dados estruturados como foram lidos,
        # antes de aplicar regras de qualidade e padronizações.
        diretorio_bronze = (
            caminho_projeto
            / "dados"
            / "bronze"
        )

        salvar_bronze_local(
            dados=dados,
            diretorio_bronze=diretorio_bronze,
            id_execucao=id_execucao,
            id_arquivo=id_arquivo,
            arquivo_origem=caminho_arquivo.name,
            fonte="anp",
        )

        dados = aplicar_regras_qualidade(
            dados
        )
        # Preparo os registros aprovados seguindo o contrato
        # definido para a camada Silver.
        dados_silver = preparar_silver(
            dados=dados,
            id_execucao=id_execucao,
            id_arquivo=id_arquivo,
            arquivo_origem=caminho_arquivo.name,
        )

        # Preparo separadamente os registros que falharam
        # nas regras de qualidade.
        dados_quarentena = preparar_quarentena(
            dados=dados,
            id_execucao=id_execucao,
            arquivo_origem=caminho_arquivo.name,
        )

        diretorio_silver = (
            caminho_projeto
            / "dados"
            / "silver"
        )

        diretorio_quarentena = (
            caminho_projeto
            / "dados"
            / "quarentena"
        )

        # Persisto somente os registros aprovados na Silver.
        salvar_silver_local(
            dados=dados_silver,
            diretorio_silver=diretorio_silver,
            id_execucao=id_execucao,
            fonte="anp",
        )

        #Crio uma visão analítica semanal a partir da Silver
        dados_gold = preparar_gold_resumo_precos(
            dados_silver
        )
        diretorio_gold = (
            caminho_projeto
            /"dados"
            /"gold"
        )
        salvar_gold_local(
            dados=dados_gold,
            diretorio_gold=diretorio_gold,
            id_execucao=id_execucao,
            nome_dataset="resumo_precos_semanais",
            fonte="anp",
        )

        # Persisto os registros rejeitados separadamente,
        # preservando os motivos de quarentena para auditoria.
        salvar_quarentena_local(
            dados=dados_quarentena,
            diretorio_quarentena=diretorio_quarentena,
            id_execucao=id_execucao,
            fonte="anp",
        )

        registros_lidos = len(dados)
        registros_aprovados = len(dados_silver)
        registros_quarentena = len(dados_quarentena)

        concluir_execucao(
            id_execucao=id_execucao,
            registros_lidos=registros_lidos,
            registros_aprovados=registros_aprovados,
            registros_quarentena=registros_quarentena,
        )

        print("Execução concluída.")
        print("Registros lidos:", registros_lidos)
        print("Registros aprovados:", registros_aprovados)
        print(
            "Registros em quarentena:",
            registros_quarentena,
        )

    except Exception as erro:
        if id_execucao is not None:
            registrar_falha(
                id_execucao=id_execucao,
                mensagem_erro=str(erro),
            )

        print("Falha durante o processamento.")
        print("Erro:", erro)

        raise


if __name__ == "__main__":
    argumentos = obter_argumentos()

    caminho_projeto = Path(__file__).resolve().parents[2]

    caminho_arquivo_padrao = (
        caminho_projeto
        / "dados"
        / "amostras"
        / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
    )

    caminho_arquivo = (
        argumentos.arquivo
        if argumentos.arquivo
        else caminho_arquivo_padrao
    )

    executar_pipeline(
        caminho_arquivo=caminho_arquivo,
        tipo_execucao=argumentos.tipo.upper(),
        permitir_reprocessamento=argumentos.reprocessar,
    )