import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def plotar_evolucao(df):
    df["data"] = pd.Timestamp.now()
    fig = px.line(df, x="data", y=["adultos", "ninfas"], labels={"value": "Quantidade", "variable": "Estágio"})
    return fig

def plotar_previsao(df):
    if "data" not in df.columns or "pop_total" not in df.columns:
        raise ValueError("DataFrame precisa conter as colunas 'data' e 'pop_total'")
    fig = px.line(df, x="data", y="pop_total", labels={"pop_total": "População Estimada", "data": "Data"})
    return fig

def plotar_comparativo(df):
    if "data" not in df.columns or not any(col in df.columns for col in ["adultos", "ninfas", "pop_total"]):
        raise ValueError("DataFrame precisa conter as colunas esperadas")
    fig = px.line(df, x="data", y=df.columns.drop("data"), labels={"value": "População", "variable": "Tipo"})
    return fig