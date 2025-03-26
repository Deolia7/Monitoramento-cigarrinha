import streamlit as st
from utils.clima import obter_previsao_clima
from utils.recomendacoes import gerar_recomendacoes
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.pdf import gerar_pdf
import pandas as pd
import os

st.set_page_config(page_title="Monitoramento da Cigarrinha", layout="wide")

st.title("🦟 Monitoramento da Cigarrinha-do-milho")

aba = st.sidebar.radio("Navegação", ["📋 Cadastro da Fazenda", "🧪 Avaliação de Campo", "📈 Resultados e Relatório"])

if "dados_talhoes" not in st.session_state:
    st.session_state.dados_talhoes = []

if aba == "📋 Cadastro da Fazenda":
    with st.form("form_fazenda"):
        st.subheader("📍 Dados da Fazenda")
        nome_fazenda = st.text_input("Nome da Fazenda")
        talhao = st.text_input("Identificação do Talhão")
        data = st.date_input("Data da Avaliação")

        st.markdown("🧭 Formato de coordenadas: `lat lon` (Ex: `-18.3908 -52.6356`)")
        local = st.text_input("Localização (cidade ou 'lat,lon')", placeholder="Ex: Goianésia ou -18.3908,-52.6356")

        imagem = st.file_uploader("📷 Anexar Foto da Avaliação", type=["jpg", "png", "jpeg"])

        submit = st.form_submit_button("Salvar Cadastro")
        if submit:
            st.session_state.cadastro = {
                "fazenda": nome_fazenda,
                "talhao": talhao,
                "data": data,
                "local": local,
                "imagem": imagem
            }
            st.success("Cadastro salvo com sucesso!")

elif aba == "🧪 Avaliação de Campo":
    if "cadastro" not in st.session_state:
        st.warning("Por favor, preencha o cadastro da fazenda antes.")
    else:
        st.subheader("🧪 Inserção dos Pontos de Coleta (mínimo 3)")
        num_pontos = st.slider("Número de pontos", 3, 5, 3)

        pontos = []
        for i in range(num_pontos):
            with st.expander(f"Ponto {i+1}"):
                adultos = st.number_input(f"Qtd. de Adultos - Ponto {i+1}", min_value=0)
                ninfas = st.number_input(f"Qtd. de Ninfas - Ponto {i+1}", min_value=0)
                pontos.append({"ponto": i+1, "adultos": adultos, "ninfas": ninfas})

        if st.button("Salvar Avaliação"):
            df = pd.DataFrame(pontos)
            df["media"] = df[["adultos", "ninfas"]].mean(axis=1)
            df["data"] = st.session_state.cadastro["data"]
            df["talhao"] = st.session_state.cadastro["talhao"]
            st.session_state.dados_talhoes.append(df)
            st.success("Avaliação salva com sucesso!")

elif aba == "📈 Resultados e Relatório":
    if not st.session_state.dados_talhoes:
        st.warning("Nenhuma avaliação registrada ainda.")
    else:
        st.subheader("📊 Evolução Populacional")
        df_talhao = pd.concat(st.session_state.dados_talhoes)
        st.plotly_chart(plotar_evolucao(df_talhao), use_container_width=True)

        st.subheader("🌦️ Previsão Populacional com Clima")
        clima_df = obter_previsao_clima(st.session_state.cadastro["local"])
        st.plotly_chart(plotar_previsao(clima_df), use_container_width=True)

        st.subheader("🤖 Recomendação Técnica")
        recomendacao = gerar_recomendacoes(df_talhao)
        st.markdown(f"**🔎 {recomendacao}**")

        st.subheader("📥 Relatório")
        if st.button("📄 Gerar Relatório em PDF"):
            pdf_file = gerar_pdf(st.session_state.cadastro, df_talhao, clima_df, recomendacao)
            st.success("Relatório gerado com sucesso!")
            st.download_button("⬇️ Baixar Relatório PDF", data=pdf_file, file_name="relatorio_cigarrinha.pdf")