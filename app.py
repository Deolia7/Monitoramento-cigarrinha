
import streamlit as st
import pandas as pd
import os
from clima import obter_previsao_clima
from recomendacoes import gerar_recomendacoes
from graficos import plotar_evolucao, plotar_previsao, plotar_comparativo

DADOS_CSV = "dados_simulados.csv"

# ------------------------ Funções auxiliares ------------------------

def carregar_dados():
    if os.path.exists(DADOS_CSV):
        return pd.read_csv(DADOS_CSV, parse_dates=["data"])
    else:
        return pd.DataFrame(columns=["fazenda", "talhao", "data", "adultos", "ninfas", "localizacao"])

def salvar_dados(novos_dados):
    df_existente = carregar_dados()
    df_atualizado = pd.concat([df_existente, novos_dados], ignore_index=True)
    df_atualizado.to_csv(DADOS_CSV, index=False)

def interface_cadastro():
    st.header("📋 Cadastro de Monitoramento")
    with st.form("formulario"):
        col1, col2 = st.columns(2)
        with col1:
            fazenda = st.text_input("Nome da Fazenda", max_chars=50)
            talhao = st.text_input("Talhão", max_chars=50)
            adultos = st.number_input("Qtd. de Adultos", 0, 1000, step=1)
        with col2:
            ninfas = st.number_input("Qtd. de Ninfas", 0, 1000, step=1)
            data = st.date_input("Data da coleta")
            localizacao = st.text_input("Localização (cidade ou coordenadas)", value="Ribeirão Preto")

        submitted = st.form_submit_button("Salvar Dados")
        if submitted:
            novos_dados = pd.DataFrame([{
                "fazenda": fazenda,
                "talhao": talhao,
                "data": pd.to_datetime(data),
                "adultos": adultos,
                "ninfas": ninfas,
                "localizacao": localizacao
            }])
            salvar_dados(novos_dados)
            st.success("✅ Dados salvos com sucesso!")

def interface_analise():
    st.title("📊 Monitoramento da Cigarrinha-do-Milho")
    df = carregar_dados()
    if df.empty:
        st.warning("Nenhum dado cadastrado ainda.")
        return

    fazendas = df["fazenda"].unique()
    fazenda_sel = st.selectbox("Selecionar fazenda", fazendas)
    talhoes = df[df["fazenda"] == fazenda_sel]["talhao"].unique()
    talhao_sel = st.selectbox("Selecionar talhão", talhoes)

    df_filtrado = df[(df["fazenda"] == fazenda_sel) & (df["talhao"] == talhao_sel)].sort_values("data")

    if df_filtrado.empty:
        st.warning("Nenhum dado para esse talhão.")
        return

    st.markdown(f"**📍 Fazenda:** {fazenda_sel} | **Talhão:** {talhao_sel}")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Adultos", int(df_filtrado["adultos"].iloc[-1]))
    col2.metric("Ninfas", int(df_filtrado["ninfas"].iloc[-1]))
    col3.metric("Data", df_filtrado["data"].iloc[-1].strftime("%d/%m/%Y"))

    st.subheader("📈 Evolução Populacional")
    plotar_evolucao(df_filtrado)

    # Previsão e clima
    st.subheader("🌦️ Previsão Populacional com Clima")
    local = df_filtrado["localizacao"].iloc[-1]
    clima_df = obter_previsao_clima(local)
    if clima_df is not None:
        plotar_previsao(df_filtrado, clima_df)
        plotar_comparativo(df_filtrado, clima_df)

    # Recomendação
    st.subheader("🤖 Recomendação Técnica")
    recomendacao = gerar_recomendacoes(df_filtrado, clima_df)
    st.info(recomendacao)

# ------------------------ Execução principal ------------------------

menu = st.sidebar.selectbox("Menu", ["Cadastrar Dados", "Análise e Recomendação"])
if menu == "Cadastrar Dados":
    interface_cadastro()
else:
    interface_analise()
