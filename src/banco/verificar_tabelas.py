from conexao_postgres import criar_conexao


def verificar_tabelas():
    """
    Consulto as tabelas públicas criadas no PostgreSQL
    para confirmar a implantação da estrutura de controle.
    """

    consulta = """
        SELECT
            table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(consulta)

            tabelas = cursor.fetchall()

    print("Tabelas encontradas:")

    for tabela in tabelas:
        print("-", tabela[0])


if __name__ == "__main__":
    verificar_tabelas()