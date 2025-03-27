import streamlit as st
import os
import pandas as pd
from utils.pdf import gerar_pdf
from utils.clima import obter_previsao_clima
from utils.recomendacoes import gerar_recomendacoes
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-milho", layout="wide")
st.title("🦟 Monitoramento da Cigarrinha-do-milho")

# Estados da aplicação
if "dados" not in st.session_state:
    st.session_state.dados = []

abas = st.tabs(["📋 Cadastro", "🧪 Avaliação", "📊 Resultados"])

with abas[0]:
    st.header("📋 Nova Avaliação de Campo")
    nome_fazenda = st.text_input("Nome da Fazenda")
    talhao = st.text_input("Identificação do Talhão")
    data = st.date_input("Data da Avaliação")
    local = st.text_input("Localização (cidade ou 'lat,lon')", placeholder="Ex: Goianésia ou 18.3907,-52.6356")
    foto = st.file_uploader("📸 Anexar Foto da Avaliação", type=["jpg", "jpeg", "png"])

    if st.button("Salvar Cadastro"):
        st.session_state.fazenda_info = {
            "nome_fazenda": nome_fazenda,
            "talhao": talhao,
            "data": str(data),
            "local": local,
            "foto": foto
        }
        st.success("Cadastro salvo com sucesso!")

with abas[1]:
    st.header("🧪 Avaliação por Pontos")
    if "fazenda_info" not in st.session_state:
        st.warning("Preencha os dados da aba anterior primeiro.")
    else:
        pontos = st.slider("Número de pontos de coleta", 3, 5, 3)
        dados = []
        for i in range(pontos):
            st.subheader(f"Ponto {i+1}")
            adultos = st.number_input(f"Quantidade de Adultos (Ponto {i+1})", min_value=0, step=1)
            ninfas = st.number_input(f"Quantidade de Ninfas (Ponto {i+1})", min_value=0, step=1)
            dados.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})
        if st.button("Salvar Avaliação"):
            for d in dados:
                d.update(st.session_state.fazenda_info)
                st.session_state.dados.append(d)
            st.success("Avaliação salva!")

with abas[2]:
    st.header("📊 Resultados")
    if not st.session_state.dados:
        st.info("Nenhuma avaliação disponível.")
    else:
        df = pd.DataFrame(st.session_state.dados)
        st.subheader("📈 Evolução Populacional")
        st.plotly_chart(plotar_evolucao(df), use_container_width=True)

        st.subheader("🌤️ Previsão Populacional com Clima")
        clima_df = obter_previsao_clima(st.session_state.fazenda_info["local"])
        st.plotly_chart(plotar_previsao(clima_df), use_container_width=True)

        st.subheader("📉 Comparativo Populacional")
        st.plotly_chart(plotar_comparativo(df), use_container_width=True)

        st.subheader("📋 Recomendações")
        recomendacoes = gerar_recomendacoes(df)
        st.markdown(recomendacoes)

        st.subheader("📄 Baixar Relatório")
        pdf_bytes = gerar_pdf(df, clima_df, recomendacoes, st.session_state.fazenda_info)
        st.download_button("📥 Baixar PDF", data=pdf_bytes, file_name="relatorio.pdf", mime="application/pdf")
