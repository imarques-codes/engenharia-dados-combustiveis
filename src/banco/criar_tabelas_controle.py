from pathlib import Path

from conexao_postgres import criar_conexao


# Localizo a raiz do projeto a partir deste script
caminho_projeto = Path(__file__).resolve().parents[2]

# Localizo o arquivo SQL responsável pela estrutura
# operacional de controle do pipeline
caminho_sql = (
    caminho_projeto
    / "sql"
    / "controle"
    / "01_criar_tabelas_controle.sql"
)


def criar_tabelas_controle():
    """
    Executo o script SQL responsável pela criação das
    tabelas operacionais utilizadas pelo pipeline.
    """

    if not caminho_sql.exists():
        raise FileNotFoundError(
            f"Arquivo SQL não encontrado: {caminho_sql}"
        )

    # Leio o script SQL preservando seu conteúdo original
    sql_tabelas = caminho_sql.read_text(
        encoding="utf-8"
    )

    # Abro a conexão com o PostgreSQL Cloud e executo
    # a criação das estruturas de controle
    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql_tabelas,
                prepare=False,
            )

        conexao.commit()

    print("Tabelas de controle criadas com sucesso.")


if __name__ == "__main__":
    criar_tabelas_controle()