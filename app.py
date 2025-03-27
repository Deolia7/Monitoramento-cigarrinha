
import streamlit as st
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.recomendacoes import gerar_recomendacoes
from utils.pdf import gerar_pdf
from utils.clima import obter_previsao_clima

st.set_page_config(layout="wide")
st.title("🦟 Monitoramento da Cigarrinha-do-milho")

abas = st.tabs(["📋 Cadastro", "📈 Evolução Populacional", "🌦️ Previsão Populacional com Clima", "📊 Comparativo", "✅ Resultado"])

with abas[0]:
    st.subheader("Cadastro da Fazenda")
    nome_fazenda = st.text_input("Nome da Fazenda")
    local = st.text_input("Localização (cidade ou 'lat,lon')", placeholder="Ex: Goianésia ou 18.39,-49.13")
    if st.button("Salvar Fazenda"):
        if nome_fazenda and local:
            st.session_state.fazenda_info = {"nome": nome_fazenda, "local": local}
            st.success("Fazenda salva com sucesso!")
        else:
            st.warning("Preencha todos os campos.")

with abas[1]:
    st.subheader("📊 Evolução Populacional")
    st.write("Insira os dados de adultos e ninfas coletados nos pontos de monitoramento.")
    pontos = [1, 2, 3]
    dados = []
    for ponto in pontos:
        col1, col2 = st.columns(2)
        with col1:
            adultos = st.number_input(f"Quantidade de Adultos (Ponto {ponto})", min_value=0, value=0, step=1)
        with col2:
            ninfas = st.number_input(f"Quantidade de Ninfas (Ponto {ponto})", min_value=0, value=0, step=1)
        dados.append({"ponto": ponto, "adultos": adultos, "ninfas": ninfas})
    if st.button("Salvar Avaliação"):
        st.session_state.avaliacao = dados
        st.success("Avaliação salva!")

    if "avaliacao" in st.session_state:
        df = plotar_evolucao(st.session_state.avaliacao)
        st.plotly_chart(df, use_container_width=True)

with abas[2]:
    st.subheader("🌦️ Previsão Populacional com Clima")
    if "fazenda_info" in st.session_state and "local" in st.session_state.fazenda_info:
        local = st.session_state.fazenda_info["local"]
        clima_df = obter_previsao_clima(local)
        if clima_df is not None:
            fig = plotar_previsao(clima_df)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não foi possível obter os dados climáticos.")
    else:
        st.warning("Localização da fazenda não encontrada.")

with abas[3]:
    st.subheader("📊 Comparativo")
    if "avaliacao" in st.session_state and "fazenda_info" in st.session_state:
        local = st.session_state.fazenda_info.get("local")
        clima_df = obter_previsao_clima(local)
        if clima_df is not None:
            fig = plotar_comparativo(st.session_state.avaliacao, clima_df)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Erro ao gerar o comparativo. Verifique os dados.")
    else:
        st.warning("Preencha os dados de avaliação e localização.")

with abas[4]:
    st.subheader("✅ Resultado e Recomendação")
    if "avaliacao" in st.session_state:
        recomendacao = gerar_recomendacoes(st.session_state.avaliacao)
        st.write("### Recomendação Técnica")
        st.write(recomendacao)
        if st.button("📥 Baixar Relatório em PDF"):
            gerar_pdf(st.session_state.fazenda_info, st.session_state.avaliacao, recomendacao)
    else:
        st.warning("Preencha os dados de avaliação.")
