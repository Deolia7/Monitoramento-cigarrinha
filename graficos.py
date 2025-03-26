
import plotly.express as px

def gerar_graficos(df):
    fig = px.line(df, x="data", y=["adultos", "ninfas"], markers=True, labels={
        "value": "Qtd. Insetos",
        "data": "Data",
        "variable": "Estágio"
    })
    fig.update_layout(legend_title_text="Estágio")
    return fig
