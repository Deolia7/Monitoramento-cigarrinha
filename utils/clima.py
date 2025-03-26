import requests
import pandas as pd
import toml

def obter_previsao_clima(local):
    config = toml.load("config.toml")
    api_key = config["openweather"]["api_key"]

    if "," in local:
        lat, lon = local.split(",")
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat.strip()}&lon={lon.strip()}&appid={api_key}&units=metric"
    else:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={local}&appid={api_key}&units=metric"

    resposta = requests.get(url).json()
    dias = {}
    for item in resposta["list"]:
        dia = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]
        if dia not in dias:
            dias[dia] = []
        dias[dia].append(temp)
    return pd.DataFrame({
        "data": dias.keys(),
        "media_temp": [sum(v)/len(v) for v in dias.values()]
    })