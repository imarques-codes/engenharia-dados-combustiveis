from src.banco.conexao_postgres import criar_conexao

def arquivo_ja_processado(id_arquivo):
    """Verifico se o arquivo já possui pelo menos uma conexão
    concluida com sucesso.
    """

    consulta = """
        SELECT EXISTS (
            SELECT 1
            FROM controle_execucao
            WHERE id_arquivo = %s
                AND status_execucao = 'CONCLUIDA'
        );
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                consulta,
                (id_arquivo,),
            )
            resultado = cursor.fetchone()
    return resultado[0]

if __name__ == "__main__":
    id_arquivo_teste = 1

    processado = arquivo_ja_processado(
        id_arquivo_teste
    )
    print("ID do arquivo:", id_arquivo_teste)
    print("Já processado:", processado)