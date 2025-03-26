def gerar_recomendacoes(previsao_df):
    picos = previsao_df[(previsao_df["adultos"] >= 10) | (previsao_df["ninfas"] >= 8)]
    if picos.empty:
        return "População sob controle. Continue monitorando regularmente."
    else:
        pico = picos.iloc[0]["data"]
        return f"🚨 Recomendado aplicar inseticida antes de {pico}, para evitar o pico populacional."