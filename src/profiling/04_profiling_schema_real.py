from pathlib import Path

import pandas as pd


# Localiza a raiz do projeto a partir da posição deste script
caminho_projeto = Path(__file__).resolve().parents[2]

# Monta o caminho até o arquivo de amostra da ANP
caminho_arquivo = (
    caminho_projeto
    / "dados"
    / "amostras"
    / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
)

# Nome da planilha onde estão os dados dos postos revendedores
nome_planilha = "POSTOS REVENDEDORES"

# O cabeçalho real da tabela está na linha 10 do Excel.
# Como o Pandas começa a contagem em zero, usamos 9.
linha_cabecalho = 9


# Faz a leitura da planilha já utilizando o cabeçalho correto
dados = pd.read_excel(
    caminho_arquivo,
    sheet_name=nome_planilha,
    header=linha_cabecalho
)


print("=" * 70)
print("PROFILING COM O CABEÇALHO REAL")
print("=" * 70)

# Mostra o tamanho real da base depois de ignorar os metadados iniciais
print(f"\nQuantidade real de registros: {dados.shape[0]:,}")
print(f"Quantidade de colunas: {dados.shape[1]}")

# Lista os nomes das colunas encontradas no arquivo
print("\nCOLUNAS:")
for numero, coluna in enumerate(dados.columns, start=1):
    print(f"{numero:02d} - {coluna}")

# Exibe os tipos que o Pandas inferiu para cada coluna
print("\nTIPOS INFERIDOS:")
print(dados.dtypes)

# Calcula aproximadamente quanto o DataFrame ocupa na memória
memoria_bytes = dados.memory_usage(deep=True).sum()
memoria_mb = memoria_bytes / (1024 ** 2)

print(f"\nMemória utilizada: {memoria_mb:.2f} MB")

# Exibe uma pequena amostra para confirmar se a leitura ficou correta
print("\nPRIMEIROS 5 REGISTROS:")
print(dados.head())