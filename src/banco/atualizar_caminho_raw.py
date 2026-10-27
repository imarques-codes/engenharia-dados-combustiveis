from pathlib import Path

from src.banco.conexao_postgres import criar_conexao


def atualizar_caminho_raw(
    id_arquivo,
    caminho_raw,
):
    """
    Atualizo o catálogo operacional com a localização
    do arquivo preservado na camada RAW.
    """

    caminho_raw = Path(caminho_raw)

    comando = """
        UPDATE controle_arquivo
        SET caminho_raw = %s
        WHERE id_arquivo = %s
        RETURNING id_arquivo, nome_arquivo, caminho_raw;
    """

    with criar_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                comando,
                (
                    caminho_raw.as_posix(),
                    id_arquivo,
                ),
            )

            resultado = cursor.fetchone()

        conexao.commit()

    if resultado is None:
        raise RuntimeError(
            f"Arquivo com ID {id_arquivo} não encontrado."
        )

    return resultado


if __name__ == "__main__":
    caminho_projeto = Path(__file__).resolve().parents[2]

    caminho_raw_absoluto = (
        caminho_projeto
        / "dados"
        / "raw"
        / "anp"
        / "f40da41fecc036126f442d6aa0e1bb423b7261aff8d8ea47fbe701b3c1ac778b"
        / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
    )

    caminho_raw_relativo = caminho_raw_absoluto.relative_to(
        caminho_projeto
    )

    resultado = atualizar_caminho_raw(
        id_arquivo=1,
        caminho_raw=caminho_raw_relativo,
    )

    print("Caminho RAW atualizado.")
    print("ID arquivo:", resultado[0])
    print("Nome:", resultado[1])
    print("RAW:", resultado[2])