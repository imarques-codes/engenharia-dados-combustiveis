from uuid import uuid4

from src.banco.conexao_postgres import criar_conexao


def iniciar_execucao(
    id_arquivo,
    tipo_execucao="INCREMENTAL",
):
    """
    Inicio uma nova execução do pipeline e retorno
    o identificador utilizado para rastreamento.
    """

    id_execucao = str(uuid4())

    comando = """
        INSERT INTO controle_execucao (
            id_execucao,
            id_arquivo,
            tipo_execucao,
            status_execucao
        )
        VALUES (%s, %s, %s, 'INICIADA');
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                comando,
                (
                    id_execucao,
                    id_arquivo,
                    tipo_execucao,
                ),
            )

        conexao.commit()

    return id_execucao


def concluir_execucao(
    id_execucao,
    registros_lidos,
    registros_aprovados,
    registros_quarentena,
):
    """
    Finalizo uma execução bem-sucedida registrando
    as principais métricas do processamento.
    """

    comando = """
        UPDATE controle_execucao
        SET
            status_execucao = 'CONCLUIDA',
            data_fim_utc = CURRENT_TIMESTAMP,
            registros_lidos = %s,
            registros_aprovados = %s,
            registros_quarentena = %s
        WHERE id_execucao = %s;
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                comando,
                (
                    registros_lidos,
                    registros_aprovados,
                    registros_quarentena,
                    id_execucao,
                ),
            )

        conexao.commit()


def registrar_falha(
    id_execucao,
    mensagem_erro,
):
    """
    Registro uma falha sem perder o histórico
    da execução que apresentou o problema.
    """

    comando = """
        UPDATE controle_execucao
        SET
            status_execucao = 'FALHA',
            data_fim_utc = CURRENT_TIMESTAMP,
            mensagem_erro = %s
        WHERE id_execucao = %s;
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                comando,
                (
                    mensagem_erro,
                    id_execucao,
                ),
            )

        conexao.commit()

def registrar_execucao_ignorada(
    id_arquivo,
    tipo_execucao="INCREMENTAL",
):
    """
    Registro uma tentativa que não precisou processar o arquivo
    porque ele já possui uma execução concluída.
    """

    id_execucao = str(uuid4())

    comando = """
        INSERT INTO controle_execucao (
            id_execucao,
            id_arquivo,
            tipo_execucao,
            status_execucao,
            data_fim_utc,
            registros_lidos,
            registros_aprovados,
            registros_quarentena
        )
        VALUES (
            %s,
            %s,
            %s,
            'IGNORADA_DUPLICIDADE',
            CURRENT_TIMESTAMP,
            0,
            0,
            0
        );
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                comando,
                (
                    id_execucao,
                    id_arquivo,
                    tipo_execucao,
                ),
            )

        conexao.commit()

    return id_execucao


if __name__ == "__main__":
    id_arquivo_teste = 1

    id_execucao = iniciar_execucao(
        id_arquivo=id_arquivo_teste,
        tipo_execucao="INCREMENTAL",
    )

    print("Execução iniciada.")
    print("ID da execução:", id_execucao)

    concluir_execucao(
        id_execucao=id_execucao,
        registros_lidos=19516,
        registros_aprovados=19515,
        registros_quarentena=1,
    )

    print("Execução concluída com sucesso.")