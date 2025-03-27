
def gerar_recomendacoes(media_adultos, media_ninfas):
    if media_adultos > 5 or media_ninfas > 10:
        return "Recomenda-se aplicação imediata de inseticida."
    elif media_adultos > 2 or media_ninfas > 5:
        return "Monitorar de perto e considerar aplicação em breve."
    else:
        return "População sob controle. Continuar monitoramento."
