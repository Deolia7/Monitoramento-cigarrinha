
def gerar_recomendacoes(df):
    media = df["adultos"].mean() + df["ninfas"].mean()
    if media > 10:
        return "⚠️ Alta infestação. Recomenda-se aplicação imediata de inseticida."
    elif media > 5:
        return "🔍 Monitoramento contínuo necessário. Avaliar nova amostragem em 5 dias."
    else:
        return "✅ População controlada. Seguir com o monitoramento semanal."
