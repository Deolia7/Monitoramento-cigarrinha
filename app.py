
import streamlit as st
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.recomendacoes import gerar_recomendacoes
from utils.pdf import gerar_pdf
from utils.clima import obter_previsao_clima
import pandas as pd

st.set_page_config(page_title="Monitoramento da Cigarrinha", layout="wide")
st.markdown("# 🦟 Monitoramento da Cigarrinha-do-milho")

# Entrada de localização
local = st.text_input(
    "Localização (cidade ou coordenadas Google)",
    placeholder="Ex: Goianesia ou 18 23 26.8S 52 38 08.3W"
)

# Simulação da coleta
st.markdown("### 📊 Evolução Populacional")
df_talhao = st.session_state.get("df_talhao", pd.DataFrame())
if not df_talhao.empty:
    st.plotly_chart(plotar_evolucao(df_talhao), use_container_width=True)
else:
    st.info("Nenhum dado disponível para exibir o gráfico.")

# Previsão com clima
st.markdown("### 🌦️ Previsão Populacional com Clima")
try:
    clima_df = obter_previsao_clima(local)
    st.plotly_chart(plotar_previsao(clima_df), use_container_width=True)
except Exception as e:
    st.warning(f"Não foi possível obter a previsão populacional: {e}")

# Comparativo
st.markdown("### 📊 Comparativo Populacional")
try:
    if not df_talhao.empty and not clima_df.empty:
        st.plotly_chart(plotar_comparativo(df_talhao, clima_df), use_container_width=True)
    else:
        st.info("Dados insuficientes para gerar gráfico comparativo.")
except Exception as e:
    st.warning(f"Não foi possível gerar o gráfico comparativo.")

# Recomendações
st.markdown("### 🧪 Recomendações Técnicas")
try:
    if not df_talhao.empty and not clima_df.empty:
        rec = gerar_recomendacoes(df_talhao, clima_df)
        st.markdown(rec)
except:
    st.warning("Não foi possível gerar recomendações.")

# PDF
if st.button("📄 Baixar relatório PDF"):
    try:
        gerar_pdf(df_talhao, clima_df, local)
        st.success("Relatório gerado com sucesso!")
    except:
        st.error("Erro ao gerar o relatório.")
