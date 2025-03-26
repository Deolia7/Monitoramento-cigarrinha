
import streamlit as st
import pandas as pd
import datetime
from utils.recomendacoes import gerar_recomendacoes
from utils.graficos import gerar_graficos
from utils.clima import obter_previsao_clima

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-Milho", layout="wide")

# Dados simulados ou carregados
df = pd.read_csv("data/dados_simulados.csv", parse_dates=["data"])

# Sidebar - Filtros
st.sidebar.title("Filtros")
fazendas = df["fazenda"].unique()
fazenda_selecionada = st.sidebar.selectbox("Selecionar fazenda", fazendas)
talhoes = df[df["fazenda"] == fazenda_selecionada]["talhao"].unique()
talhao_selecionado = st.sidebar.selectbox("Selecionar talhão", talhoes)

# Filtrar dados
dados_filtrados = df[(df["fazenda"] == fazenda_selecionada) & (df["talhao"] == talhao_selecionado)]

# Última observação
dados_atuais = dados_filtrados.sort_values("data").iloc[-1]

st.title("📊 Monitoramento da Cigarrinha-do-Milho")
st.markdown(f"### 🧭 Fazenda: {fazenda_selecionada} | Talhão: {talhao_selecionado}")
col1, col2, col3 = st.columns(3)
col1.metric("Adultos", int(dados_atuais["adultos"]))
col2.metric("Ninfas", int(dados_atuais["ninfas"]))
col3.metric("Data", dados_atuais["data"].strftime("%d/%m/%Y"))

st.markdown("---")
st.subheader("📈 Evolução Populacional")
st.plotly_chart(gerar_graficos(dados_filtrados), use_container_width=True)

# Recomendação
st.subheader("🤖 Recomendação Técnica")
previsao = obter_previsao_clima()
mensagem = gerar_recomendacoes(dados_filtrados, previsao)
st.info(mensagem)

st.markdown("---")
st.caption("Desenvolvido para fins de demonstração com dados simulados.")
