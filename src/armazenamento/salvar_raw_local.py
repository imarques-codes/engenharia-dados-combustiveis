import shutil
from pathlib import Path

from src.ingestao.calcular_hash_arquivo import calcular_hash_sha256


def salvar_arquivo_raw(
    caminho_origem,
    diretorio_raw,
    fonte="anp",
):
    """
    Preservo o arquivo original na camada RAW utilizando
    o SHA-256 como identidade técnica do conteúdo.
    """

    caminho_origem = Path(caminho_origem)
    diretorio_raw = Path(diretorio_raw)

    if not caminho_origem.exists():
        raise FileNotFoundError(
            f"Arquivo de origem não encontrado: {caminho_origem}"
        )

    hash_origem = calcular_hash_sha256(
        caminho_origem
    )

    # Organizo a RAW pelo hash para não misturar conteúdos diferentes
    # que eventualmente tenham o mesmo nome de arquivo.
    diretorio_arquivo = (
        diretorio_raw
        / fonte.lower()
        / hash_origem
    )

    diretorio_arquivo.mkdir(
        parents=True,
        exist_ok=True,
    )

    caminho_destino = (
        diretorio_arquivo
        / caminho_origem.name
    )

    if caminho_destino.exists():
        hash_destino = calcular_hash_sha256(
            caminho_destino
        )

        if hash_destino != hash_origem:
            raise RuntimeError(
                "O arquivo existente na RAW possui conteúdo "
                "diferente do arquivo de origem."
            )

        print("Arquivo já existe na RAW.")
        print("Caminho:", caminho_destino)

        return caminho_destino

    # Copio o arquivo sem alterar seu conteúdo original.
    shutil.copy2(
        caminho_origem,
        caminho_destino,
    )

    hash_destino = calcular_hash_sha256(
        caminho_destino
    )

    if hash_destino != hash_origem:
        caminho_destino.unlink(missing_ok=True)

        raise RuntimeError(
            "Falha na validação de integridade do arquivo copiado para a RAW."
        )

    print("Arquivo salvo na RAW.")
    print("Caminho:", caminho_destino)
    print("SHA-256:", hash_destino)

    return caminho_destino


if __name__ == "__main__":
    caminho_projeto = Path(__file__).resolve().parents[2]

    caminho_origem = (
        caminho_projeto
        / "dados"
        / "amostras"
        / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
    )

    diretorio_raw = (
        caminho_projeto
        / "dados"
        / "raw"
    )

    salvar_arquivo_raw(
        caminho_origem=caminho_origem,
        diretorio_raw=diretorio_raw,
        fonte="anp",
    )