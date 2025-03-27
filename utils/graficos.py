
import pandas as pd
import plotly.express as px

def plotar_evolucao(df):
    df["data"] = pd.Timestamp.now()
    df_long = df.melt(id_vars=["data"], value_vars=["adultos", "ninfas"], var_name="Estágio", value_name="Qtd. Insetos")
    return px.line(df_long, x="data", y="Qtd. Insetos", color="Estágio", markers=True)

def plotar_previsao(df):
    df["data"] = pd.to_datetime(df["data"])
    df["pop_total"] = df["temp"] * 0.2 + df["umidade"] * 0.05
    return px.line(df, x="data", y="pop_total", title="Previsão Populacional (Baseada no Clima)")

def plotar_comparativo(df_real, df_prev):
    df_real["fonte"] = "observado"
    df_prev["fonte"] = "previsto"
    df_prev = df_prev.rename(columns={"pop_total": "valor"})
    df_real = df_real.rename(columns={"adultos": "valor"})
    df_real["data"] = pd.to_datetime("today")
    df_prev["data"] = pd.to_datetime(df_prev["data"])
    df_comparado = pd.concat([df_real[["data", "valor", "fonte"]], df_prev[["data", "valor", "fonte"]]])
    return px.line(df_comparado, x="data", y="valor", color="fonte", markers=True)
