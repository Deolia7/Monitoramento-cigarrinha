import streamlit as st

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-milho", layout="wide")

st.title("🚨 Monitoramento da Cigarrinha-do-milho")
local = st.text_input("Localização (cidade ou coordenadas Google)", placeholder="Ex: Goianésia ou 18°23'26.8\"S 52°38'08.3\"W")

if local:
    st.success(f"Localização registrada: {local}")
    st.markdown("### 📊 Evolução Populacional")
    st.info("Gráfico de evolução seria exibido aqui.")

    st.markdown("### 🌦️ Previsão Populacional com Clima")
    st.info("Gráfico de previsão com clima seria exibido aqui.")

    st.markdown("### 📈 Comparativo Populacional")
    st.info("Gráfico comparativo seria exibido aqui.")

    st.markdown("### 🧪 Recomendações Técnicas")
    st.info("Recomendações técnicas baseadas nos dados seriam exibidas aqui.")
