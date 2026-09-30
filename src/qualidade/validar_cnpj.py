import re

def limpar_cnpj(cnpj):
    """
    Limpo caracteres de formatação e padronizo o CNPJ
    para letras maiúsculas
    """

    if cnpj is None:
        return None

    cnpj = str(cnpj).strip().upper()

    #Removo pontos, barras, hífens, espaços e outros caracteres que não fazem parte do identificador
    cnpj = re.sub(r"[^A-Z0-9]", "", cnpj)

    return cnpj

def normalizar_cnpj(cnpj):
    """
    Normalizo CNPJs numéricos antigos que perderam zeros á esquerda durante
    a leitura da fonte    
    """

    cnpj = limpar_cnpj(cnpj)

    if not cnpj:
        return None

    #Completo zeros á esquerda somente quando o valor
    # é totalmente numérico e possui menos de 14 posições 
    if cnpj.isdigit() and len(cnpj) < 14:
        cnpj = cnpj.zfill(14)

    return cnpj

def converter_caractere_para_valor(caractere):
    """
    Converto cada caractere para o valor utilizado
    no cálculo oficial do dígito verificador
    """

    return ord(caractere) - 48

def calcular_digito_verificador(base, pesos):
    """
    Calculo um dígito verificador utilizando módulo 11.
    """

    soma = 0

    for caractere, peso in zip(base, pesos):
        valor = converter_caractere_para_valor(caractere)
        soma += valor * peso

    resto = soma % 11

    if resto in (0, 1):
        return "0"

    return str(11 - resto)

def validar_cnpj(cnpj):
    """
    Valido CNPJs numéricos e alfanuméricos utilizando
    os dois dígitos verificadores
    """

    cnpj = normalizar_cnpj(cnpj)

    if cnpj is None:
        return False

    #O CNPJ precisa possuir exatamente 14 posições 
    if len(cnpj) != 14:
        return False

    #As doze primeiras posições podem conter letras ou números
    base = cnpj[:12]

    if not base.isalnum():
        return False

    #Os dois dígitos verificadores permanencem numéricos
    digitos_informados = cnpj[12:]

    if not digitos_informados.isdigit():
        return False

     # Evito aceitar identificadores evidentemente inválidos,
    # como uma sequência formada somente por zeros
    if len(set(cnpj)) == 1:
        return False

    pesos_primeiro_digito = [
        5, 4, 3, 2,
        9, 8, 7, 6,
        5, 4, 3, 2,
    ]

    primeiro_digito = calcular_digito_verificador(
        base,
        pesos_primeiro_digito,
    )

    pesos_segundo_digito = [
        6, 5, 4, 3, 2,
        9, 8, 7, 6,
        5, 4, 3, 2,
    ]

    segundo_digito = calcular_digito_verificador(
        base + primeiro_digito,
        pesos_segundo_digito,
    )

    digitos_calculados = primeiro_digito + segundo_digito

    return digitos_informados == digitos_calculados


if __name__ == "__main__":

    # Testo um CNPJ numérico que perdeu zeros à esquerda
    cnpj_teste_numerico = "198451000185"

    print("CNPJ numérico:")
    print("Original:", cnpj_teste_numerico)
    print("Normalizado:", normalizar_cnpj(cnpj_teste_numerico))
    print("Válido:", validar_cnpj(cnpj_teste_numerico))

    print("-" * 60)

    # Testo o formato alfanumérico atual
    cnpj_teste_alfanumerico = "00.000.000/E08G-12"

    print("CNPJ alfanumérico:")
    print("Original:", cnpj_teste_alfanumerico)
    print(
        "Normalizado:",
        normalizar_cnpj(cnpj_teste_alfanumerico),
    )
    print(
        "Válido:",
        validar_cnpj(cnpj_teste_alfanumerico),
    )
