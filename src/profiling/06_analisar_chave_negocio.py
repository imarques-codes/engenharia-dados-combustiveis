from pathlib import Path
import pandas as pd

#Localizo a raiz do projeto a partir deste script
caminho_projeto = Path(__file__).resolve().parents[2]

#Defino o arquivo que vou utilizar na análise
caminho_arquivo = (
    caminho_projeto
    / "dados"
    / "amostras"
    / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
)

nome_planilha = "POSTOS REVENDEDORES"
linha_cabecalho = 9

#Preservo CNPJ e CEP como identificadores textuais
tipos_identificadores ={
    "CNPJ": "string",
    "CEP": "string",
}

#Carrego os dados utilizando o cabecalho real da planilha
dados = pd.read_excel(
    caminho_arquivo,
    sheet_name=nome_planilha,
    header=linha_cabecalho,
    dtype=tipos_identificadores,

)
print("=" * 70)
print("ANÁLISE DE CHAVE NEGÓCIO")
print("=" * 70)

#Defino CNPJ, produto e data como primeira linha hipótese de chave de negócio
colunas_chave = [
    "CNPJ",
    "PRODUTO",
    "DATA DA COLETA",
]

#Identifico todos os registros envolvidos em repetições da chave candidata
registros_repetidos = dados[
    dados.duplicated(
        subset=colunas_chave,
        keep=False,
    )
].copy()

print(f"\nTotal de registros: {len(dados):,}")

print(
    "Registros envolvidos em repetição da chave candidata: "
    f"{len(registros_repetidos):}"
)

#Conto quantas vezes cada combinação da chave aparece na base
quantidade_por_chave = (
    dados
    .groupby(
        colunas_chave,
        dropna=False,
    )
    .size()
    .reset_index(name="quantidade")
)

#Mantenho somente as chaves que aparecem mais de euma vez
chaves_repetidas = quantidade_por_chave[
    quantidade_por_chave["quantidade"] > 1
]

print(
    "Quantidade de chaves repetidas: "
    f"{len(chaves_repetidas):,}"
)

#Analiso possíveis conflitos somente se existirem chaves repetidas
if not registros_repetidos.empty:
    #Verifico de a mesma chave aparece associada a mais de um preço
    conflitos_preco = (
        registros_repetidos
        .groupby(
            colunas_chave,
            dropna=False,
        )["PREÇO DE REVENDA"]
        .nunique()
        .reset_index(name="quantidade_precos")
    )

    conflitos_preco = conflitos_preco[
        conflitos_preco["quantidade_precos"] > 1 
    ]

    print(
        "Chaves wrepetidas com preços diferentes: "
        f"{len(conflitos_preco):,}"
    )

    #Exibo alguns exemplos para entender o padrão das repetições
    print("\nEXEMPLOS DE REGISTROS REPETIDOS: ")

    print(
        registros_repetidos[
            colunas_chave
            + [
                "PREÇO DE REVENDA",
                "MUNICIPIO",
                "ESTADO",
            ]
        ]
        .sort_values(colunas_chave)
        .head(20)
        .to_string(index=False)
    )

else:
    print("Não encontrei repetição para a chave candidata")