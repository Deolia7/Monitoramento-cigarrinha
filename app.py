
import streamlit as st
import pandas as pd
import json
import datetime
import pytz
import altair as alt

st.set_page_config(layout="wide")
st.title("📊 Monitoramento da Cigarrinha-do-Milho")

# Carregar os dados
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("https://raw.githubusercontent.com/Deolia7/Monitoramento-cigarrinha/main/dados_monitoramento.csv")
        df["data"] = pd.to_datetime(df["data"])
        return df
    except:
        st.error("Erro ao carregar os dados.")
        return pd.DataFrame()

df = carregar_dados()
if df.empty:
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Filtros")
    fazendas = df["fazenda"].unique()
    fazenda_sel = st.selectbox("Selecionar fazenda", fazendas)

    talhoes = df[df["fazenda"] == fazenda_sel]["talhao"].unique()
    talhao_sel = st.selectbox("Selecionar talhão", talhoes)

    st.markdown("---")
    st.caption("Desenvolvido para fins de demonstração com dados simulados.")

# Filtrar dados
df_filtro = df[(df["fazenda"] == fazenda_sel) & (df["talhao"] == talhao_sel)]

# Métricas
st.subheader(f"📍 Fazenda: {fazenda_sel} | Talhão: {talhao_sel}")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Adultos", int(df_filtro["adultos"].iloc[-1]))
with col2:
    st.metric("Ninfas", int(df_filtro["ninfas"].iloc[-1]))
with col3:
    st.metric("Data", df_filtro["data"].dt.strftime("%d/%m/%Y").iloc[-1])

# Gráficos
st.markdown("### Evolução Populacional")
base = alt.Chart(df_filtro).encode(x="data:T")
adultos_line = base.mark_line(color="orange").encode(y="adultos:Q")
ninfas_line = base.mark_line(color="blue").encode(y="ninfas:Q")
st.altair_chart(adultos_line + ninfas_line, use_container_width=True)

# Tabela
st.markdown("### Histórico de Coletas")
st.dataframe(df_filtro[["data", "adultos", "ninfas"]].sort_values("data", ascending=False), use_container_width=True)
