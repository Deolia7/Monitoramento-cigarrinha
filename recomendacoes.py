
def gerar_recomendacoes(df, clima):
    dados_atuais = df.sort_values("data").iloc[-1]
    adultos = dados_atuais["adultos"]
    ninfas = dados_atuais["ninfas"]

    msg = ""
    if adultos + ninfas >= 15:
        msg += "⚠️ Alerta de Infestação Alta. "
    elif adultos + ninfas >= 10:
        msg += "🟠 População moderada, acompanhe nos próximos dias. "
    else:
        msg += "🟢 População controlada. "

    if clima and clima.get("rain", 0) > 2:
        msg += "Previsão de chuva significativa nos próximos dias."

    return msg
