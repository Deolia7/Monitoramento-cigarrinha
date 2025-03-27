
import streamlit as st
import pandas as pd
from utils.graficos import plotar_evolucao, plotar_previsao, plotar_comparativo
from utils.recomendacoes import gerar_recomendacoes
from utils.pdf import gerar_pdf
from utils.clima import obter_previsao_clima

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-milho", layout="wide")

st.markdown("# 🦟 Monitoramento da Cigarrinha-do-milho")

if "fazenda_info" not in st.session_state:
    st.session_state.fazenda_info = {}

st.subheader("🧪 Evolução Populacional")
df = pd.DataFrame(st.session_state.get("dados_talhao", []))

if not df.empty:
    st.plotly_chart(plotar_evolucao(df), use_container_width=True)
else:
    st.info("Nenhum dado disponível para exibir o gráfico.")

st.subheader("🌦️ Previsão Populacional com Clima")
try:
    clima_df = obter_previsao_clima(st.session_state.fazenda_info["local"])
    st.plotly_chart(plotar_previsao(clima_df), use_container_width=True)
except Exception as e:
    st.warning(f"Não foi possível obter a previsão populacional: {e}")

st.subheader("📊 Comparativo Populacional")
try:
    st.plotly_chart(plotar_comparativo(df, clima_df), use_container_width=True)
except:
    st.warning("Não foi possível gerar o gráfico comparativo.")

st.subheader("🧪 Recomendações Técnicas")
try:
    recomendacoes = gerar_recomendacoes(df, clima_df)
    for rec in recomendacoes:
        st.success(rec)
except:
    st.warning("Não foi possível gerar recomendações.")

st.subheader("📄 Gerar Relatório em PDF")
if st.button("📥 Baixar Relatório"):
    try:
        pdf_bytes = gerar_pdf(df, clima_df, recomendacoes)
        st.download_button(label="📥 Clique para baixar o PDF",
                           data=pdf_bytes,
                           file_name="relatorio_cigarrinha.pdf",
                           mime="application/pdf")
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
