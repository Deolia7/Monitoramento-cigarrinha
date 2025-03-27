import streamlit as st

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-milho", layout="wide")
st.title("🦟 Monitoramento da Cigarrinha-do-milho")

# Exemplo de estrutura da interface (resumida)
local = st.text_input("Localização (cidade ou coordenadas Google)", placeholder="Ex: Goianésia ou 18°23'26.8"S 52°38'08.3"W")

if local:
    st.success("Interface carregada com sucesso.")
    st.subheader("📈 Evolução Populacional")
    st.info("Gráfico de evolução aqui")

    st.subheader("🌦️ Previsão Populacional com Clima")
    st.info("Gráfico de previsão com clima")

    st.subheader("📊 Comparativo Populacional")
    st.info("Gráfico comparativo")

    st.subheader("🧪 Recomendações Técnicas")
    st.success("Recomendações baseadas nos dados")

    st.download_button("📥 Baixar Relatório em PDF", data="PDF gerado", file_name="relatorio.pdf")
