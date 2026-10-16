def avaliar_qualidade_registro(
    cnpj_valido,
    cep_formato_valido,
):
    """
    Avalio as regras críticas de qualidade de um registro
    e retorno o status junto com todos os motivos de rejeição.
    """

    motivos_quarentena = []

    # Registro a violação sem interromper a avaliação porque uma mesma linha pode possuir mais de um problema
    if not cnpj_valido:
        motivos_quarentena.append("CNPJ_INVALIDO")

    if not cep_formato_valido:
        motivos_quarentena.append("CEP_SUSPEITO")

    # Se nenhuma regra crítica foi violada, permito que o registro continue no fluxo para a Silver
    if not motivos_quarentena:
        return "APROVADO", None

    # Preservo todos os motivos encontrados
    motivos = "|".join(motivos_quarentena)

    return "QUARENTENA", motivos


if __name__ == "__main__":
    exemplos = [
        (True, True),
        (False, True),
        (True, False),
        (False, False),
    ]

    for cnpj_valido, cep_valido in exemplos:
        status, motivo = avaliar_qualidade_registro(
            cnpj_valido,
            cep_valido,
        )

        print("-" * 60)
        print("CNPJ válido:", cnpj_valido)
        print("CEP válido:", cep_valido)
        print("Status:", status)
        print("Motivo:", motivo)