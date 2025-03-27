
# Arquivo principal do app (simplificado para ilustração)
import streamlit as st
from utils.clima import obter_previsao_clima
from utils.recomendacoes import gerar_recomendacoes
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.pdf import gerar_pdf
import pandas as pd

st.set_page_config(page_title="Monitoramento da Cigarrinha", layout="wide")
aba = st.sidebar.selectbox("Selecione a aba", ["Cadastro da Fazenda", "Avaliação do Talhão", "Resultados"])

if "dados" not in st.session_state:
    st.session_state["dados"] = []
if "imagem" not in st.session_state:
    st.session_state["imagem"] = None

if aba == "Cadastro da Fazenda":
    with st.form("form_fazenda"):
        nome = st.text_input("Nome da Fazenda")
        talhao = st.text_input("Identificação do Talhão")
        imagem = st.file_uploader("Foto do Talhão", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Salvar Cadastro")
        if submitted:
            st.session_state["nome"] = nome
            st.session_state["talhao"] = talhao
            st.session_state["imagem"] = imagem
            st.success("Cadastro salvo com sucesso!")

elif aba == "Avaliação do Talhão":
    with st.form("form_avaliacao"):
        data = st.date_input("Data da Avaliação")
        local = st.text_input("Localização (cidade ou 'lat,lon')", placeholder="Ex: Goianesia ou 18.3908,-52.6356")
        pontos = st.slider("Número de Pontos de Coleta", 3, 5, 3)
        coleta = []
        for i in range(pontos):
            adultos = st.number_input(f"Adultos no ponto {i+1}", min_value=0, step=1)
            ninfas = st.number_input(f"Ninfas no ponto {i+1}", min_value=0, step=1)
            coleta.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})
        submit = st.form_submit_button("Salvar Avaliação")
        if submit:
            st.session_state["dados"] = coleta
            st.session_state["data"] = data
            st.session_state["local"] = local
            st.success("Dados salvos com sucesso!")

elif aba == "Resultados":
    if st.session_state["dados"]:
        df = pd.DataFrame(st.session_state["dados"])
        st.subheader("📊 Evolução Populacional")
        st.plotly_chart(plotar_evolucao(df), use_container_width=True)

        st.subheader("🌦️ Previsão Populacional com Clima")
        clima_df = obter_previsao_clima(st.session_state["local"])
        st.plotly_chart(plotar_previsao(clima_df), use_container_width=True)

        st.subheader("📉 Comparativo por Ponto de Coleta")
        st.plotly_chart(plotar_comparativo(df), use_container_width=True)

        st.subheader("🤖 Recomendação Técnica")
        st.write(gerar_recomendacoes(df))

        st.download_button("📥 Baixar Relatório em PDF", gerar_pdf(df, clima_df, st.session_state["imagem"]), file_name="relatorio.pdf")
    else:
        st.warning("Preencha os dados da avaliação primeiro.")
