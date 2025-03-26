
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Monitoramento da Cigarrinha-do-Milho", layout="centered")

st.title("🌽 Monitoramento da Cigarrinha-do-Milho")

# Identificação do Talhão
st.subheader("📝 Identificação do Talhão")
talhao = st.text_input("Nome do Talhão")
data_avaliacao = st.date_input("Data da Avaliação", value=datetime.date.today())
estagio = st.selectbox("Estágio Fenológico", ["V2", "V3", "V4", "V5", "V6", "VT", "R1", "R2", "Outro"])

# Registro dos pontos
st.subheader("📌 Registro por Ponto Amostral")

num_pontos = 4
dados = []

for ponto in range(1, num_pontos + 1):
    st.markdown(f"**Ponto {ponto}**")
    ninfas = st.number_input(f"Ninfas por Planta - Ponto {ponto}", min_value=0.0, step=0.1, key=f"ninfa_{ponto}")
    adultos = st.number_input(f"Adultos por Planta - Ponto {ponto}", min_value=0.0, step=0.1, key=f"adulto_{ponto}")
    dados.append({"Ponto": f"Ponto {ponto}", "Ninfas": ninfas, "Adultos": adultos})

# Processamento dos dados
df = pd.DataFrame(dados)

media_ninfas = df["Ninfas"].mean()
media_adultos = df["Adultos"].mean()

# Avaliação de risco
def classificar_risco(n, a):
    if a > 1.5 or n > 2.0:
        return "ALTO", "Aplicar inseticida imediatamente"
    elif a > 0.8 or n > 1.0:
        return "MÉDIO", "Reavaliar em 3 dias"
    else:
        return "BAIXO", "Acompanhar"

nivel_risco, recomendacao = classificar_risco(media_ninfas, media_adultos)

# Resultados
st.subheader("📊 Resultados")

col1, col2 = st.columns(2)
col1.metric("Média de Ninfas", f"{media_ninfas:.2f}")
col2.metric("Média de Adultos", f"{media_adultos:.2f}")

st.success(f"Nível de Risco: **{nivel_risco}**")
st.info(f"Recomendação: **{recomendacao}**")

# Download dos dados
st.download_button("⬇️ Baixar Dados em Excel", data=df.to_csv(index=False).encode("utf-8"),
                   file_name="monitoramento_cigarrinha.csv", mime="text/csv")
