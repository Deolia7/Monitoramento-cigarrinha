import streamlit as st
import pandas as pd
from utils.clima import obter_previsao_clima
from utils.recomendacoes import gerar_recomendacoes
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.pdf import gerar_pdf
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-Milho", layout="wide")

st.title("📊 Monitoramento da Cigarrinha-do-Milho")

# Carregamento dos dados
if "dados" not in st.session_state:
    st.session_state.dados = []

# Sidebar - Cadastro
st.sidebar.header("📋 Nova Avaliação de Campo")
with st.sidebar.form("formulario"):
    fazenda = st.text_input("Nome da Fazenda")
    talhao = st.text_input("Identificação do Talhão")
    data = st.date_input("Data da Avaliação", value=datetime.today())
    adultos = st.number_input("Quantidade de Adultos", min_value=0, step=1)
    ninfas = st.number_input("Quantidade de Ninfas", min_value=0, step=1)
    local = st.text_input("Localização (cidade ou 'lat,lon')", help="Ex: Ribeirão Preto ou -21.17,-47.81")
    imagem = st.file_uploader("📷 Anexar Foto da Avaliação", type=["jpg", "jpeg", "png"])
    enviado = st.form_submit_button("Salvar Avaliação")
    if enviado:
        st.session_state.dados.append({
            "Fazenda": fazenda,
            "Talhão": talhao,
            "Data": data,
            "Adultos": adultos,
            "Ninfas": ninfas,
            "Local": local,
            "Imagem": imagem.name if imagem else None
        })
        st.success("Avaliação salva com sucesso!")
        if imagem:
            os.makedirs("fotos", exist_ok=True)
            with open(os.path.join("fotos", imagem.name), "wb") as f:
                f.write(imagem.getbuffer())

# Conversão para DataFrame
df = pd.DataFrame(st.session_state.dados)

# Interface de visualização
if not df.empty:
    st.subheader("📈 Evolução Populacional")
    plotar_evolucao(df)

    st.subheader("🌤️ Previsão Populacional com Clima")
    local = df.iloc[-1]["Local"]
    adultos = df.iloc[-1]["Adultos"]
    ninfas = df.iloc[-1]["Ninfas"]
    clima_df = obter_previsao_clima(local)
    previsao_df = plotar_previsao(clima_df, adultos, ninfas)
    st.dataframe(previsao_df)

    st.subheader("📊 Comparativo com Histórico")
    plotar_comparativo(previsao_df, df)

    st.subheader("🤖 Recomendação Técnica")
    recomendacao = gerar_recomendacoes(previsao_df)
    st.success(recomendacao)

    st.subheader("📄 Exportar Relatório em PDF")
    if st.button("📥 Gerar PDF"):
        gerar_pdf(df, previsao_df, recomendacao)
        with open("relatorio_final.pdf", "rb") as pdf_file:
            b64 = base64.b64encode(pdf_file.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="relatorio_final.pdf">📄 Clique para baixar o relatório</a>'
            st.markdown(href, unsafe_allow_html=True)