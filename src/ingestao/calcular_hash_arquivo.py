import hashlib
from pathlib import Path
def calcular_hash_sha256(caminho_arquivo):
    """
    Calculo o hash SHA-256 do conteúdo de um arquivo para identificar
    duplicidades e controlar a indempotência da ingestão
    """
    caminho_arquivo = Path (caminho_arquivo)

    # Interrompo o processamento caso o arquivo informado não exista
    if not caminho_arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho_arquivo}"
        )

    hash_sha256 = hashlib.sha256()

    # Leio o arquivo em blocos para não precisar carregá-lo interno na memório 
    # quando trabalhar com arquivos menores

    with caminho_arquivo.open("rb") as arquivo:
        for bloco in iter(
            lambda: arquivo.read(1024 * 1024),
            b"",
        ):
            hash_sha256.update(bloco)
    return hash_sha256.hexdigest()

if __name__ == "__main__":
    caminho_projeto = Path(__file__).resolve().parents[2]

    caminho_arquivo = (

        caminho_projeto
        /"dados"
        /"amostras"
        / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
    )

    hash_arquivo = calcular_hash_sha256(caminho_arquivo)

    print("Arquivo:", caminho_arquivo.name)
    print("SHA-256:", hash_arquivo)