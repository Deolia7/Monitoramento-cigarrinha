
import streamlit as st
import pandas as pd
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.recomendacoes import gerar_recomendacoes
from utils.pdf import gerar_pdf
from utils.clima import obter_previsao_clima

st.set_page_config(layout="wide")
st.title("🦟 Monitoramento da Cigarrinha-do-milho")

abas = st.tabs(["📋 Cadastro", "📈 Avaliação", "✅ Resultados"])

with abas[0]:
    st.subheader("Cadastro da Fazenda")
    nome_fazenda = st.text_input("Nome da Fazenda")
    local = st.text_input("Localização (cidade ou coordenadas Google)", placeholder="Ex: Goianésia ou 18°23'26.8"S 52°38'08.3"W")
    imagem = st.file_uploader("📸 Enviar imagem do talhão (opcional)", type=["jpg", "jpeg", "png"])

    if st.button("Salvar Fazenda"):
        if nome_fazenda and local:
            st.session_state.fazenda_info = {"nome": nome_fazenda, "local": local, "imagem": imagem}
            st.success("Fazenda salva!")
        else:
            st.warning("Preencha todos os campos.")

with abas[1]:
    st.subheader("Preencher Avaliação")
    if "avaliacoes" not in st.session_state:
        st.session_state.avaliacoes = []

    n_pontos = st.slider("Número de pontos avaliados", 3, 5, 3)
    pontos = []
    for i in range(n_pontos):
        with st.expander(f"Ponto {i+1}"):
            adultos = st.number_input(f"Adultos no ponto {i+1}", min_value=0, value=0)
            ninfas = st.number_input(f"Ninfas no ponto {i+1}", min_value=0, value=0)
            pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

    if st.button("Salvar Avaliação"):
        st.session_state.avaliacoes = pontos
        st.success("Dados de campo salvos com sucesso!")

with abas[2]:
    st.subheader("📊 Resultados e Recomendação")
    if "avaliacoes" in st.session_state and "fazenda_info" in st.session_state:
        df = pd.DataFrame(st.session_state.avaliacoes)
        local = st.session_state.fazenda_info["local"]
        clima_df = obter_previsao_clima(local)

        st.plotly_chart(plotar_evolucao(df), use_container_width=True)
        st.plotly_chart(plotar_previsao(clima_df), use_container_width=True)
        st.plotly_chart(plotar_comparativo(df, clima_df), use_container_width=True)

        st.subheader("📌 Recomendação Técnica")
        rec = gerar_recomendacoes(df)
        for r in rec:
            st.success(r)

        st.subheader("📄 Gerar Relatório")
        if st.button("📥 Baixar PDF"):
            gerar_pdf(st.session_state.fazenda_info, df, clima_df, rec)
    else:
        st.warning("Cadastre a fazenda e salve os dados de avaliação.")
