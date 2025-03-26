
import matplotlib.pyplot as plt

def plotar_evolucao(df):
    fig, ax = plt.subplots()
    df.plot(x='data', y=['adultos', 'ninfas'], ax=ax)
    return fig

def plotar_previsao(df):
    fig, ax = plt.subplots()
    df.plot(x='data', y='pop_total', ax=ax)
    return fig

def plotar_comparativo(df):
    fig, ax = plt.subplots()
    df.groupby('talhao')['adultos'].mean().plot(kind='bar', ax=ax)
    return fig
