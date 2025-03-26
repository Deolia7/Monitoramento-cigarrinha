
def gerar_recomendacoes(media_adultos, media_ninfas):
    if media_adultos + media_ninfas > 10:
        return "Aplicar inseticida imediatamente para evitar o pico populacional."
    return "Monitorar mais alguns dias antes da aplicação."
