from pathlib import Path

import pandas as pd


caminho_projeto = Path(__file__).resolve().parents[2]

caminho_arquivo = (
    caminho_projeto
    / "dados"
    / "amostras"
    / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
)

nome_planilha = "POSTOS REVENDEDORES"


dados_brutos = pd.read_excel(
    caminho_arquivo,
    sheet_name=nome_planilha,
    header=None,
    nrows=20
)


print("=" * 80)
print("INSPEÇÃO DAS PRIMEIRAS LINHAS DO ARQUIVO")
print("=" * 80)

for indice, linha in dados_brutos.iterrows():

    valores = [
        str(valor)
        for valor in linha.tolist()
        if pd.notna(valor)
    ]

    print(f"\nLinha {indice}:")
    print(valores)