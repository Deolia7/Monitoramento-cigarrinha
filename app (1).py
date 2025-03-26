
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cigarrinha do Milho - Previsão & Controle", layout="wide")
st.title("🌽 Painel Inteligente - Cigarrinha do Milho")

# Função para buscar temperatura atual via OpenWeatherMap
def get_temperature(city, api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        response = requests.get(url)
        data = response.json()
        return data["main"]["temp"]
    except:
        return None

# Entrada de dados básicos
with st.sidebar:
    st.header("📍 Local e Dados Climáticos")
    city = st.text_input("Cidade (ex: Lucas do Rio Verde, BR)", value="Lucas do Rio Verde, BR")
    api_key = st.text_input("🔑 Sua API Key OpenWeather", type="password")
    temperatura = None
    if city and api_key:
        temperatura = get_temperature(city, api_key)
        if temperatura:
            st.success(f"🌡️ Temp. atual: {temperatura:.1f}°C")
        else:
            st.warning("⚠️ Não foi possível obter a temperatura.")

st.subheader("🦟 Monitoramento de Campo")
data_avaliacao = st.date_input("Data da Avaliação", value=datetime.date.today())
estagio = st.selectbox("Estágio Fenológico", ["V2", "V3", "V4", "V5", "V6", "VT", "R1", "R2", "Outro"])
adultos = st.number_input("Adultos por planta (média)", min_value=0.0, step=0.1)
ninfas = st.number_input("Ninfas por planta (média)", min_value=0.0, step=0.1)

if temperatura is not None and (adultos > 0 or ninfas > 0):

    # Conversão de ninfas em adultos baseada na temperatura
    if temperatura >= 28:
        conv = 0.8
    elif temperatura >= 24:
        conv = 0.7
    else:
        conv = 0.5

    futuros_adultos = adultos + (ninfas * conv)

    # Parâmetros do modelo logístico
    K = 3.0  # capacidade máxima (ajustável)
    P0 = futuros_adultos
    r = 0.4 if temperatura >= 28 else (0.3 if temperatura >= 24 else 0.2)
    dias = np.arange(0, 11)
    P = K / (1 + ((K - P0) / P0) * np.exp(-r * dias))

    # Recomendação baseada na curva
    dias_critico = np.where(P >= 1.5)[0]
    if len(dias_critico) == 0:
        risco = "BAIXO"
        acao = "Acompanhar"
    elif dias_critico[0] <= 3:
        risco = "ALTO"
        acao = "Aplicar inseticida imediatamente"
    else:
        risco = "MÉDIO"
        acao = "Reavaliar em 2 dias"

    col1, col2 = st.columns(2)
    col1.metric("Adultos observados", f"{adultos:.2f}")
    col2.metric("Ninfas observadas", f"{ninfas:.2f}")
    st.info(f"🔁 População futura estimada: **{futuros_adultos:.2f} adultos/planta**")

    st.subheader("📈 Projeção da População (Modelo Logístico)")
    fig, ax = plt.subplots()
    ax.plot(dias, P, marker='o', label='Adultos previstos')
    ax.axhline(1.5, color='red', linestyle='--', label='Nível crítico (1.5)')
    ax.set_xlabel("Dias a partir da avaliação")
    ax.set_ylabel("Adultos por planta")
    ax.set_title("Projeção de Crescimento Populacional")
    ax.legend()
    st.pyplot(fig)

    st.subheader("🚨 Recomendação Técnica")
    st.success(f"Nível de Risco: **{risco}**")
    st.warning(f"Recomendação: **{acao}**")

    st.caption("📚 Fonte: EMBRAPA (2012), UFV, Lopes & Gallo (2002), dados adaptados.")

else:
    st.info("🔎 Insira cidade, API Key e dados de campo para gerar previsões.")
