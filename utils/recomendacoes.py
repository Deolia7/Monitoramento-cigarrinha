def gerar_recomendacoes(adultos, ninfas):
    total = adultos + ninfas
    if total >= 6:
        return "Aplicar inseticida imediatamente para conter a infestação."
    elif 3 <= total < 6:
        return "Monitorar diariamente. Considerar aplicação se o clima for favorável à praga."
    else:
        return "População sob controle. Reavaliar em 3 dias."