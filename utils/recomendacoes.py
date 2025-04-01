def gerar_recomendacoes(dados, populacao_prevista):
    pico = max(populacao_prevista)
    recomendacoes = []

    if pico > 20:
        recomendacoes.append("Alerta crítico: considerar aplicação imediata de inseticida.")
    elif pico > 10:
        recomendacoes.append("Atenção: tendência de aumento populacional. Monitore frequentemente e considere aplicação preventiva.")
    else:
        recomendacoes.append("População sob controle. Continuar monitoramento.")

    recomendacoes.append("Produto recomendado: Efficon (Dalbulus maidis)")
    recomendacoes.append("Dose: 800 a 1000 mL p.c./ha")
    recomendacoes.append("Calda Terrestre: 150 L/ha")
    recomendacoes.append("Aplicar no início da infestação. Repetir se houver reinfestação.")
    recomendacoes.append("Intervalo de aplicação: Máximo 3 aplicações com intervalo de 7 dias.")
    recomendacoes.append("Intervalo de segurança: 35 dias.")

    return recomendacoes