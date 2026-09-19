from pathlib import Path

import pandas as pd

caminho_projeto = Path(__file__).resolve().parents[2]

caminho_arquivo = (
    caminho_projeto
    /"dados"
    /"amostras"
    /"revendas_lpc_2026-09-06_2026-09-12.xlsx"
)
nome_planilha = "POSTOS REVENDEDORES"

dados = pd.read_excel(
    caminho_arquivo,
    sheet_name=nome_planilha
)

print("=" * 60)
print("PROFILING ESTRUTURAL")
print("=" * 60)

print(f"\nQuantidade de linhas: {dados.shape[0]:,}")
print(f"Quantidade de colunas: {dados.shape[1]}")

print("\nCOLUNAS ENCONTRADAS:")
for numero, coluna in enumerate(dados.columns, start=1):
    print(f"{numero:02d} - {coluna}")

print("\nTIPOS INDERIDOS PELO PANDAS:")
print(dados.dtypes)

memoria_bytes = dados.memory_usage(deep=True).sum()
memoria_mb = memoria_bytes / (1024 ** 2)

print(f"\nMemória utilizada pelo DataFrame: {memoria_mb:.2f} MB")

print("\nPRIMEIROS 5 REGISTROS:")
print(dados.head())