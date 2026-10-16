from src.banco.conexao_postgres import criar_conexao


def verificar_execucoes():
    """
    Consulto as execuções registradas no PostgreSQL
    para validar o histórico operacional do pipeline.
    """

    consulta = """
        SELECT
            id_execucao,
            id_arquivo,
            tipo_execucao,
            status_execucao,
            data_inicio_utc,
            data_fim_utc,
            registros_lidos,
            registros_aprovados,
            registros_quarentena,
            mensagem_erro
        FROM controle_execucao
        ORDER BY data_inicio_utc DESC;
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(consulta)

            execucoes = cursor.fetchall()

    print("EXECUÇÕES REGISTRADAS")
    print("-" * 80)

    for execucao in execucoes:
        (
            id_execucao,
            id_arquivo,
            tipo_execucao,
            status_execucao,
            data_inicio,
            data_fim,
            registros_lidos,
            registros_aprovados,
            registros_quarentena,
            mensagem_erro,
        ) = execucao

        print("ID execução:", id_execucao)
        print("ID arquivo:", id_arquivo)
        print("Tipo:", tipo_execucao)
        print("Status:", status_execucao)
        print("Início:", data_inicio)
        print("Fim:", data_fim)
        print("Registros lidos:", registros_lidos)
        print("Registros aprovados:", registros_aprovados)
        print("Registros em quarentena:", registros_quarentena)
        print("Erro:", mensagem_erro)
        print("-" * 80)


if __name__ == "__main__":
    verificar_execucoes()