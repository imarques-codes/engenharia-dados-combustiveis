from pathlib import Path
import pandas as pd

#Localizo a raiz do projeto
caminho_projeto = Path(__file__).resolve().parents[2]

#Defino arquivo que vou utilizar na investigação
caminho_arquivo = (
    caminho_projeto
    / "dados"
    / "amostras"
    / "revendas_lpc_2026-09-06_2026-09-12.xlsx"
)

nome_planilha = "POSTOS REVENDEDORES"
linha_cabecalho = 9

#Preservo CNPJ e CEP como texto para não tratar
#Identificadores como medidas numéricas

tipos_identificadores = {
    "CNPJ": "string",
    "CEP": "string",
}

#Carrego os dados utilizados o cabeçalho real da planilha
dados = pd.read_excel(
    caminho_arquivo,
    sheet_name=nome_planilha,
    header=linha_cabecalho,
    dtype=tipos_identificadores,
)

print("=" * 70)
print("ANÁLISE DE CNPJ E CEP")
print("=" * 70)

#CNPJ

#Removo espaços desnecessários para analisar o conteúdo recebido
cnpj_original = dados["CNPJ"].str.strip()

#Verifico se existem CNPjs contendo caracteres diferentees de números
cnpj_nao_numerico = cnpj_original[
    ~cnpj_original.str.fullmatch(r"\d+", na=False)
]

print("\nCNPJ")
print("-" * 70)
print(
    "Valores com caracteres não númericos: "
    f"{len(cnpj_nao_numerico):,}"
)

#Testo a hipótese de que os dígitos ausentes são zeros á esquerda
#Não altero a coluna original da base
cnpj_normalizado = cnpj_original.str.zfill(14)

#Verifico se algum valor continua fora das 14 posições esperadas
cnpj_tamanho_invalido = cnpj_normalizado[
    cnpj_normalizado.str.len() != 14
]
print(
    "CNPJs fora de 14 posições após normalização"
    f"{len(cnpj_tamanho_invalido):,}"
)

#Comparo o valor recebido com a versão temporariamenter normalizada
amostra_cnpj = pd.DataFrame({
    "cnpj_original": cnpj_original,
    "cnpj_normalizado": cnpj_normalizado,
})

#Mantenho somente os CNPs que chegaram com menos de 14 dígitos
amostra_cnpj = amostra_cnpj[
    amostra_cnpj["cnpj_original"].str.len() < 14
]

print("\nEXEMPLOS DE CNPJ:")
print(
    amostra_cnpj
    .drop_duplicates()
    .head(20)
    .to_string(index=False)
)

#CEP

#Removo espaços desnecessários antes de analisar os CEPs
cep_original = dados["CEP"].str.strip()

#Verifico se existem caracteres diferentes de números
cep_nao_numerico = cep_original[
    ~cep_original.str.fullmatch(r"\d+", na=False)
]

print("\nCEP")
print("-" * 70)

print(
"Valores com caracteres não numéricos: "
f"{len(cep_nao_numerico):,}"
)

#Testo a recuperaçao de zero á esquerda para oito posições
cep_normalizado = cep_original.str.zfill(8)

#Verifico se algum CEP continua com tamanho diferente de oito
cep_tamanho_invalido = cep_normalizado[
    cep_normalizado.str.len() != 8
]

print(
    "CEPs fora de 8 posições após normalização: "
    f"{len(cep_tamanho_invalido):,}"
)

#Crio uma visão auxiliar para investigar os CEPs suspeitos
ceps_suspeitos = pd.DataFrame({
    "cep_original": cep_original,
    "cep_normalizado": cep_normalizado,
    "municipio": dados["MUNICÍPIO"],
    "estado": dados["ESTADO"],
    "cnpj": dados["CNPJ"],
})

#Seleciono os registros cujo CEP original não possui 8 digitos
ceps_suspeitos = ceps_suspeitos[
    ceps_suspeitos["cep_original"].str.len() != 8
]

print("\nDISTRIBUIÇÃO DOS TAMNHOS ORIGINAIS")
print(
    cep_original
    .str.len()
    .value_counts()
    .sort_index()

)

print("\nEXEMPLOS DE CEP:")

print(
    ceps_suspeitos
    .drop_duplicates()
    .head(20)
    .to_string(index=False)

)

# Investigo separadamente CEPs muito pequenos porque esses casos
# podem representar erro real, e não apenas perda de zero à esquerda
ceps_muito_curtos = ceps_suspeitos[
    ceps_suspeitos["cep_original"].str.len() <= 2
]


print("\nCEPs COM TAMANHO MUITO PEQUENO:")

if ceps_muito_curtos.empty:
    print("Não encontrei CEPs com dois dígitos ou menos.")
else:
    print(
        ceps_muito_curtos
        .drop_duplicates()
        .to_string(index=False)
    )