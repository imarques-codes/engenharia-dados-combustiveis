from pathlib import Path

from src.banco.conexao_postgres import criar_conexao
from src.ingestao.calcular_hash_arquivo import calcular_hash_sha256


def registrar_arquivo(
    caminho_arquivo,
    fonte="ANP",
):
    """
    Registro um arquivo no controle operacional utilizando
    seu conteúdo como identidade técnica por meio do SHA-256.
    """

    caminho_arquivo = Path(caminho_arquivo)

    if not caminho_arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho_arquivo}"
        )

    # Calculo o hash a partir do conteúdo real do arquivo
    hash_sha256 = calcular_hash_sha256(caminho_arquivo)

    # Registro também o tamanho para apoiar auditoria
    tamanho_bytes = caminho_arquivo.stat().st_size

    comando_insercao = """
        INSERT INTO controle_arquivo (
            nome_arquivo,
            hash_sha256,
            fonte,
            tamanho_bytes
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (hash_sha256)
        DO NOTHING
        RETURNING id_arquivo;
    """

    consulta_existente = """
        SELECT
            id_arquivo
        FROM controle_arquivo
        WHERE hash_sha256 = %s;
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                comando_insercao,
                (
                    caminho_arquivo.name,
                    hash_sha256,
                    fonte,
                    tamanho_bytes,
                ),
            )

            resultado = cursor.fetchone()

            if resultado:
                id_arquivo = resultado[0]

                print("Novo arquivo registrado.")
                print("ID do arquivo:", id_arquivo)

            else:
                # Se o hash já existir, recupero o registro existente
                # em vez de cadastrar o mesmo conteúdo novamente
                cursor.execute(
                    consulta_existente,
                    (hash_sha256,),
                )

                id_arquivo = cursor.fetchone()[0]

                print("Arquivo já cadastrado.")
                print("ID existente:", id_arquivo)

        conexao.commit()

    print("Nome:", caminho_arquivo.name)
    print("SHA-256:", hash_sha256)
    print("Tamanho em bytes:", tamanho_bytes)

    return id_arquivo


if __name__ == "__main__":
    caminho_projeto = Path(__file__).resolve().parents[2]

    caminho_arquivo = (
        caminho_projeto
        / "dados"
        / "amostras"
        / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
    )

    registrar_arquivo(caminho_arquivo)