import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def plotar_evolucao(df):
    df_agg = df.groupby("Data")[["Adultos", "Ninfas"]].mean().reset_index()
    df_agg = pd.melt(df_agg, id_vars="Data", var_name="Estágio", value_name="Qtde")
    st.line_chart(data=df_agg, x="Data", y="Qtde", color="Estágio")

def plotar_previsao(previsao_df, adultos, ninfas):
    previsao_df["adultos"] = [adultos + i for i in range(len(previsao_df))]
    previsao_df["ninfas"] = [ninfas + i//2 for i in range(len(previsao_df))]
    st.line_chart(previsao_df.set_index("data")[["adultos", "ninfas"]])
    return previsao_df

def plotar_comparativo(previsao_df, historico_df):
    historico = historico_df[["Data", "Adultos", "Ninfas"]].rename(columns={"Data": "data"})
    comparativo = pd.concat([
        historico.set_index("data"),
        previsao_df[["data", "adultos", "ninfas"]].rename(columns={"adultos": "Adultos", "ninfas": "Ninfas"}).set_index("data")
    ])
    st.line_chart(comparativo)