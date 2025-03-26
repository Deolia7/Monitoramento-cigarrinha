
import matplotlib.pyplot as plt
import pandas as pd

def plotar_evolucao(df):
    fig, ax = plt.subplots()
    df_plot = df[['data', 'adultos', 'ninfas']].copy()
    df_plot = df_plot.sort_values(by='data')
    df_plot.set_index('data', inplace=True)
    df_plot.plot(ax=ax, marker='o')
    ax.set_title('Evolução Populacional')
    ax.set_ylabel('Qtd. Insetos')
    ax.set_xlabel('Data')
    ax.grid(True)
    return fig

def plotar_previsao(df_previsto):
    fig, ax = plt.subplots()
    df_previsto = df_previsto.sort_values(by='data')
    df_previsto.set_index('data', inplace=True)
    df_previsto[['adultos_previstos', 'ninfas_previstas']].plot(ax=ax, marker='o', linestyle='--')
    ax.set_title('Previsão Futura de Infestação')
    ax.set_ylabel('Qtd. Insetos (Previstos)')
    ax.set_xlabel('Data')
    ax.grid(True)
    return fig

def plotar_comparativo(df_comparativo):
    fig, ax = plt.subplots()
    df_comparativo = df_comparativo.sort_values(by='data')
    df_comparativo.set_index('data', inplace=True)
    df_comparativo[['adultos', 'adultos_previstos']].plot(ax=ax, marker='o', linestyle='-')
    df_comparativo[['ninfas', 'ninfas_previstas']].plot(ax=ax, marker='s', linestyle='--')
    ax.set_title('Comparativo: Observado x Previsto')
    ax.set_ylabel('Qtd. Insetos')
    ax.set_xlabel('Data')
    ax.grid(True)
    return fig
