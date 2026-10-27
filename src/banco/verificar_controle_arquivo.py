from src.banco.conexao_postgres import criar_conexao


def verificar_controle_arquivo():
    """
    Consulto o catálogo de arquivos para validar
    os metadados registrados no PostgreSQL.
    """

    consulta = """
        SELECT
            id_arquivo,
            nome_arquivo,
            hash_sha256,
            fonte,
            tamanho_bytes,
            caminho_raw,
            data_primeiro_registro_utc
        FROM controle_arquivo
        ORDER BY id_arquivo;
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(consulta)

            arquivos = cursor.fetchall()

    print("ARQUIVOS REGISTRADOS")
    print("-" * 80)

    for arquivo in arquivos:
        (
            id_arquivo,
            nome_arquivo,
            hash_sha256,
            fonte,
            tamanho_bytes,
            caminho_raw,
            data_registro,
        ) = arquivo

        print("ID arquivo:", id_arquivo)
        print("Nome:", nome_arquivo)
        print("SHA-256:", hash_sha256)
        print("Fonte:", fonte)
        print("Tamanho em bytes:", tamanho_bytes)
        print("RAW:", caminho_raw)
        print("Registrado em:", data_registro)
        print("-" * 80)


if __name__ == "__main__":
    verificar_controle_arquivo()