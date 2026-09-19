from pathlib import Path

import pandas as pd


# Localizo a raiz do projeto a partir deste script
caminho_projeto = Path(__file__).resolve().parents[2]

# Defino o arquivo de amostra que vou utilizar no profiling
caminho_arquivo = (
    caminho_projeto
    / "dados"
    / "amostras"
    / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
)

nome_planilha = "POSTOS REVENDEDORES"
linha_cabecalho = 9


# Leio CNPJ e CEP como texto porque são identificadores.
# Dessa forma, evito perder possíveis zeros à esquerda.
tipos_identificadores = {
    "CNPJ": "string",
    "CEP": "string",
}


# Carrego os dados preservando os identificadores como texto
dados = pd.read_excel(
    caminho_arquivo,
    sheet_name=nome_planilha,
    header=linha_cabecalho,
    dtype=tipos_identificadores,
)


print("=" * 70)
print("PROFILING DE QUALIDADE DOS DADOS")
print("=" * 70)


# -------------------------------------------------------------------
# Visão geral
# -------------------------------------------------------------------

# Verifico o volume total de registros e colunas da base
print(f"\nTotal de registros: {len(dados):,}")
print(f"Total de colunas: {len(dados.columns)}")


# -------------------------------------------------------------------
# Valores nulos
# -------------------------------------------------------------------

# Contabilizo quantos valores nulos existem em cada coluna
quantidade_nulos = dados.isna().sum()

# Calculo também o percentual de nulos para facilitar a análise
percentual_nulos = (
    quantidade_nulos
    .div(len(dados))
    .mul(100)
    .round(2)
)

resumo_nulos = pd.DataFrame({
    "quantidade_nulos": quantidade_nulos,
    "percentual_nulos": percentual_nulos,
})

# Exibo somente as colunas que realmente possuem valores ausentes
resumo_nulos = resumo_nulos[
    resumo_nulos["quantidade_nulos"] > 0
].sort_values(
    by="quantidade_nulos",
    ascending=False
)

print("\nVALORES NULOS:")
print(resumo_nulos)


# -------------------------------------------------------------------
# Duplicidades
# -------------------------------------------------------------------

# Neste momento verifico somente linhas totalmente idênticas.
# Ainda não removo nada porque primeiro preciso entender a origem delas.
quantidade_duplicados = dados.duplicated().sum()

print("\nDUPLICIDADES:")
print(f"Linhas completamente duplicadas: {quantidade_duplicados:,}")


# -------------------------------------------------------------------
# Cardinalidade
# -------------------------------------------------------------------

print("\nCARDINALIDADE:")

colunas_categoricas = [
    "ESTADO",
    "MUNICÍPIO",
    "BANDEIRA",
    "PRODUTO",
    "UNIDADE DE MEDIDA",
]

# Verifico quantos valores distintos existem nas principais colunas categóricas
for coluna in colunas_categoricas:
    quantidade_valores = dados[coluna].nunique(dropna=True)

    print(
        f"{coluna}: "
        f"{quantidade_valores:,} valores distintos"
    )


# -------------------------------------------------------------------
# Produtos encontrados
# -------------------------------------------------------------------

# Contabilizo a quantidade de registros por produto
produtos = (
    dados["PRODUTO"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nPRODUTOS ENCONTRADOS:")
print(produtos)


# -------------------------------------------------------------------
# Relação entre produto e unidade de medida
# -------------------------------------------------------------------

# Verifico se cada produto está associado à unidade de medida esperada
produto_unidade = (
    dados[
        ["PRODUTO", "UNIDADE DE MEDIDA"]
    ]
    .drop_duplicates()
    .sort_values(
        by=["PRODUTO", "UNIDADE DE MEDIDA"]
    )
)

print("\nPRODUTO X UNIDADE DE MEDIDA:")
print(produto_unidade.to_string(index=False))


# -------------------------------------------------------------------
# Estatísticas de preço
# -------------------------------------------------------------------

# Analiso inicialmente a distribuição geral dos preços de revenda
print("\nESTATÍSTICAS DE PREÇO:")
print(
    dados["PREÇO DE REVENDA"]
    .describe()
)


# Analiso os preços separadamente por produto porque existem
# combustíveis com unidades de medida diferentes.
estatisticas_produto = (
    dados
    .groupby("PRODUTO")["PREÇO DE REVENDA"]
    .agg(
        quantidade="count",
        preco_minimo="min",
        preco_medio="mean",
        preco_mediano="median",
        preco_maximo="max",
    )
    .round(2)
)

print("\nESTATÍSTICAS DE PREÇO POR PRODUTO:")
print(estatisticas_produto)


# -------------------------------------------------------------------
# Período das coletas
# -------------------------------------------------------------------

# Verifico a menor e a maior data presentes no arquivo
data_minima = dados["DATA DA COLETA"].min()
data_maxima = dados["DATA DA COLETA"].max()

print("\nPERÍODO DAS COLETAS:")
print(f"Primeira data: {data_minima}")
print(f"Última data:   {data_maxima}")


# -------------------------------------------------------------------
# Identificadores
# -------------------------------------------------------------------

# Contabilizo quantos CNPJs distintos existem na amostra
quantidade_cnpjs = dados["CNPJ"].nunique(dropna=True)

print("\nIDENTIFICADORES:")
print(f"CNPJs distintos: {quantidade_cnpjs:,}")


# Verifico o tamanho dos CNPJs exatamente como foram lidos.
# Com isso, consigo identificar possíveis problemas de formatação.
tamanhos_cnpj = (
    dados["CNPJ"]
    .dropna()
    .str.len()
    .value_counts()
    .sort_index()
)

print("\nQUANTIDADE DE DÍGITOS DOS CNPJs:")
print(tamanhos_cnpj)


# Faço a mesma validação para os CEPs
tamanhos_cep = (
    dados["CEP"]
    .dropna()
    .str.len()
    .value_counts()
    .sort_index()
)

print("\nQUANTIDADE DE DÍGITOS DOS CEPs:")
print(tamanhos_cep)