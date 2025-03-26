
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.recomendacoes import gerar_recomendacoes
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.clima import obter_previsao_clima

# Título
st.title("🌽 Monitoramento da Cigarrinha-do-Milho")

# Dados simulados
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["fazenda", "talhao", "ponto", "data", "adultos", "ninfas", "lat", "lon"])

# Cadastro
with st.form("formulario"):
    st.subheader("📋 Cadastro de Dados de Campo")
    fazenda = st.text_input("Nome da Fazenda")
    talhao = st.text_input("Nome do Talhão")
    data = st.date_input("Data", datetime.today())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        adultos = st.number_input("Qtd. de Adultos", min_value=0, step=1)
    with col2:
        ninfas = st.number_input("Qtd. de Ninfas", min_value=0, step=1)
    with col3:
        ponto = st.selectbox("Ponto de Coleta", ["Ponto 1", "Ponto 2", "Ponto 3", "Ponto 4", "Ponto 5"])
    
    col4, col5 = st.columns(2)
    with col4:
        lat = st.text_input("Latitude")
    with col5:
        lon = st.text_input("Longitude")

    submitted = st.form_submit_button("Salvar Dados")
    if submitted:
        novo_dado = {
            "fazenda": fazenda,
            "talhao": talhao,
            "ponto": ponto,
            "data": data,
            "adultos": adultos,
            "ninfas": ninfas,
            "lat": lat,
            "lon": lon
        }
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([novo_dado])], ignore_index=True)
        st.success("✅ Dados salvos com sucesso!")

# Filtro
st.sidebar.header("Filtros")
fazendas = st.session_state.df["fazenda"].unique().tolist()
fazenda_sel = st.sidebar.selectbox("Selecionar Fazenda", fazendas if fazendas else [""])
talhoes = st.session_state.df[st.session_state.df["fazenda"] == fazenda_sel]["talhao"].unique().tolist()
talhao_sel = st.sidebar.selectbox("Selecionar Talhão", talhoes if talhoes else [""])

# Dados filtrados
df_talhao = st.session_state.df[(st.session_state.df["fazenda"] == fazenda_sel) & (st.session_state.df["talhao"] == talhao_sel)]

if not df_talhao.empty:
    st.subheader("📈 Evolução Populacional")
    st.plotly_chart(plotar_evolucao(df_talhao))

    st.subheader("🌦️ Previsão Populacional com Clima")
    try:
        local = df_talhao[["lat", "lon"]].dropna().iloc[0]
        clima_df = obter_previsao_clima(local)
        st.plotly_chart(plotar_previsao(clima_df))
    except Exception as e:
        st.warning("Erro ao obter previsão climática. Verifique os dados de latitude e longitude.")

    st.subheader("📊 Comparativo Populacional por Ponto")
    st.plotly_chart(plotar_comparativo(df_talhao))

    st.subheader("🤖 Recomendação Técnica")
    recomendacao = gerar_recomendacoes(df_talhao)
    st.info(recomendacao)
else:
    st.warning("Nenhum dado cadastrado ainda para essa fazenda e talhão.")
