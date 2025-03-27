
import plotly.express as px

def plotar_evolucao(df):
    df["data"] = pd.Timestamp.now()
    return px.line(df.melt(id_vars=["ponto"], value_vars=["adultos", "ninfas"]), x="ponto", y="value", color="variable")

def plotar_previsao(df):
    return px.line(df, x="data", y="pop_total", title="Previsão Populacional")

def plotar_comparativo(df):
    return px.bar(df, x="ponto", y=["adultos", "ninfas"], barmode="group")
