from pathlib import Path

import pandas as pd

caminho_projeto = Path(__file__).resolve().parents[2]

caminho_arquivo = (
    caminho_projeto
    /"dados"
    /"amostras"
    /"revendas_lpc_2026-09-06_2026-09-12.xlsx"
)

print("Arquivo encontrado:", caminho_arquivo.exists())
print("Caminho:", caminho_arquivo)

arquivo_excel = pd.ExcelFile(caminho_arquivo)

print("\nPlanilhas encontradas:")
print(arquivo_excel.sheet_names)