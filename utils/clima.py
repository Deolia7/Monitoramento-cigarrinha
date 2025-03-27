
import requests
import pandas as pd
from datetime import datetime, timedelta
import toml

def obter_previsao_clima(local):
    config = toml.load("config.toml")
    chave = config["openweather"]["api_key"]
    if "," in local:
        lat, lon = local.split(",")
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={chave}&units=metric"
    else:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={local}&appid={chave}&units=metric"
    resp = requests.get(url)
    dados = resp.json()
    base = []
    for item in dados["list"][:30]:
        dt = datetime.fromtimestamp(item["dt"])
        base.append({"data": dt, "pop_total": (item["main"]["temp"] % 10) + 1})
    return pd.DataFrame(base)
