import streamlit as st
import pandas as pd
import os
from utils.clima import obter_previsao_clima
from utils.recomendacoes import gerar_recomendacoes
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.pdf import gerar_pdf

st.set_page_config(page_title="Monitoramento Cigarrinha", layout="wide")
st.title("🛰️ Monitoramento da Cigarrinha-do-Milho")

abas = st.tabs(["📋 Cadastro da Fazenda", "🔍 Avaliação de Campo", "📊 Resultados"])

with abas[0]:
    st.header("📋 Cadastro da Fazenda")
    nome_fazenda = st.text_input("Nome da Fazenda")
    talhao = st.text_input("Identificação do Talhão")
    local = st.text_input("Localização (cidade ou 'lat,lon')", placeholder="Ex: Goianésia ou 18°23'26.8"S 52°38'08.3"W")
    foto_avaliacao = st.file_uploader("📷 Anexar Foto da Avaliação", type=["png", "jpg", "jpeg"])
    st.session_state["dados_fazenda"] = {
        "fazenda": nome_fazenda,
        "talhao": talhao,
        "local": local,
        "foto": foto_avaliacao
    }

with abas[1]:
    st.header("🔍 Nova Avaliação de Campo")
    st.markdown("Informe os dados de até 5 pontos de coleta:")

    pontos = []
    for i in range(5):
        with st.expander(f"🧪 Ponto de Coleta {i+1}", expanded=(i < 3)):
            col1, col2 = st.columns(2)
            with col1:
                adultos = st.number_input(f"Quantidade de Adultos - Ponto {i+1}", min_value=0, value=0)
            with col2:
                ninfas = st.number_input(f"Quantidade de Ninfas - Ponto {i+1}", min_value=0, value=0)
            if adultos or ninfas:
                pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

    if st.button("Salvar Avaliação"):
        if not pontos:
            st.warning("Preencha ao menos 1 ponto de coleta.")
        elif not st.session_state.get("dados_fazenda"):
            st.warning("Preencha os dados da aba de cadastro.")
        else:
            dados = st.session_state["dados_fazenda"]
            df = pd.DataFrame(pontos)
            df["data"] = pd.to_datetime("today").date()
            df["fazenda"] = dados["fazenda"]
            df["talhao"] = dados["talhao"]
            df["local"] = dados["local"]
            st.session_state["avaliacao"] = df
            st.success("Avaliação salva com sucesso! Vá até a aba Resultados para visualizar.")

with abas[2]:
    st.header("📊 Resultados e Recomendação Técnica")

    if "avaliacao" not in st.session_state:
        st.warning("Nenhuma avaliação encontrada. Cadastre na aba anterior.")
    else:
        df = st.session_state["avaliacao"]
        st.subheader("📈 Evolução Populacional")
        st.plotly_chart(plotar_evolucao(df))

        st.subheader("🌦️ Previsão Populacional com Clima")
        clima_df = obter_previsao_clima(df["local"].iloc[0])
        st.plotly_chart(plotar_previsao(clima_df))

        st.subheader("📊 Comparativo Populacional")
        st.plotly_chart(plotar_comparativo(df, clima_df))

        st.subheader("🤖 Recomendação Técnica")
        recomendacao = gerar_recomendacoes(df, clima_df)
        st.success(recomendacao)

        st.subheader("📄 Gerar Relatório em PDF")
        if st.button("📥 Baixar Relatório"):
            foto = st.session_state["dados_fazenda"].get("foto")
            gerar_pdf(df, clima_df, recomendacao, foto)