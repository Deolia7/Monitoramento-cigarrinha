import requests
import pandas as pd
from datetime import datetime
import configparser

def obter_previsao_clima(local, adultos, ninfas):
    config = configparser.ConfigParser()
    config.read("config.toml")
    api_key = config["openweather"]["api_key"]

    if "," in local:
        lat, lon = local.split(",")
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat.strip()}&lon={lon.strip()}&appid={api_key}&units=metric&lang=pt_br"
    else:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={local}&appid={api_key}&units=metric&lang=pt_br"

    response = requests.get(url)
    dados = response.json()

    previsoes = []
    for item in dados["list"]:
        data = datetime.fromtimestamp(item["dt"])
        temp = item["main"]["temp"]
        chuva = item.get("rain", {}).get("3h", 0)
        previsoes.append({"data": data, "temperatura": temp, "chuva": chuva})

    df = pd.DataFrame(previsoes)
    df["data"] = pd.to_datetime(df["data"]).dt.date
    agrupado = df.groupby("data").agg({"temperatura": "mean", "chuva": "sum"}).reset_index()

    agrupado["pop_adultos"] = adultos
    agrupado["pop_ninfas"] = ninfas
    agrupado["pop_total"] = agrupado["pop_adultos"] + agrupado["pop_ninfas"]

    return agrupado