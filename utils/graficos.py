import pandas as pd
import matplotlib.pyplot as plt

def plotar_evolucao(df):
    df["data"] = pd.Timestamp.now()
    ax = df.plot(x="data", y=["adultos", "ninfas"])
    return ax.get_figure()

def plotar_previsao(df):
    df["data"] = pd.to_datetime(df["data"])
    ax = df.plot(x="data", y="pop_total", title="Previsão Populacional")
    return ax.get_figure()

def plotar_comparativo(df_real, df_prev):
    df_real["tipo"] = "real"
    df_prev["tipo"] = "previsto"
    df = pd.concat([df_real.rename(columns={"adultos": "pop"}), df_prev.rename(columns={"pop_total": "pop"})])
    ax = df.plot(x="data", y="pop", title="Comparativo Real x Previsto", color=["blue" if t=="real" else "orange" for t in df["tipo"]])
    return ax.get_figure()