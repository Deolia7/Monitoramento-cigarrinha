
def gerar_recomendacoes(df):
    media_pop = df["pop_total"].mean()
    pico = df["pop_total"].max()
    if pico > 20 or media_pop > 15:
        return "🚨 Aplicar inseticida imediatamente para evitar perdas!"
    elif pico > 10:
        return "⚠️ Atenção: monitorar diariamente e considerar aplicação."
    else:
        return "✅ Nível de população controlado. Sem necessidade de aplicação agora."
