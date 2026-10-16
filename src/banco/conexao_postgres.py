import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Localizo a raiz do projeto para carregar as variáveis de ambiente
caminho_projeto = Path(__file__).resolve().parents[2]

# Carrego as credenciais armazenadas somente no ambiente local
load_dotenv(caminho_projeto / ".env")


def criar_conexao():
    """
    Crio uma conexão com o PostgreSQL utilizando a URL
    armazenada fora do código-fonte.
    """

    url_banco = os.getenv("DATABASE_URL")

    if not url_banco:
        raise RuntimeError(
            "A variável DATABASE_URL não foi encontrada."
        )

    return psycopg.connect(url_banco)


if __name__ == "__main__":
    # Testo a conexão sem exibir senha ou string de conexão
    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    current_database(),
                    version();
                """
            )

            banco, versao = cursor.fetchone()

            print("Conexão com PostgreSQL realizada com sucesso.")
            print("Banco:", banco)
            print("Versão:", versao)