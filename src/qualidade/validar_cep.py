def limpar_cep(cep):
    """
    Limpo espaços e preparo o CEP recebido para validação
    """

    if cep is None:
        return None

    cep = str(cep).strip()

    if not cep:
        return None

    return cep

def classificar_cep(cep):
    """
    Classifico o CEP conforme a qualidade do valor recebido.
    """

    cep = limpar_cep(cep)
    if cep is None:
        return "AUSENTE"

    #Verifico se o valor possui somente números
    if not cep.isdigit():
        return "CARACTERE_INVALIDO"

    #Considero 8 posições como o formato estrurural esperado
    if len(cep) == 8:
        if cep == "00000000":
            return "SUSPEITO"

        return "FORMATO_VALIDO"

    #Trato 7 posições como possível perda de zero a esquerda
    if len(cep) == 7:
        return "NORMALIZAVEL" 

    #Evito mascarar problemas completando zeros em valores muito curtos
    return "SUSPEITO"

def normalizar_cep(cep):
    #Normalizo somente ceps cuja correção é considerada segura

    cep = limpar_cep(cep)
    if cep is None:
        return None

    status = classificar_cep(cep)
    if status == "NORMALIZAVEL":
        return cep.zfill(8)
    if status == "FORMATO_VALIDO":
        return cep
    return None

def validar_formato_cep(cep):
    #Verifico se o cep possui formato válido depois da normalização

    cep_normalizado = normalizar_cep(cep)
    if cep_normalizado is None:
        return False
    return (
        len(cep_normalizado) == 8
        and cep_normalizado.isdigit()
        and cep_normalizado != "00000000"
    )

if __name__ == "__main__":
    exemplos = [
        "15600000",
        "6713100",
        "0",
        "00000000",
        None,
    ]

    for cep in exemplos:
        print("-" * 50)
        print("Original:", cep)
        print("Status:", classificar_cep(cep))
        print("Normalizado:", normalizar_cep(cep))
        print("Formato válido:", validar_formato_cep(cep))