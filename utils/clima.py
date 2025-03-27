
import requests
import pandas as pd
import configparser
import re

def converter_coordenadas(coord_str):
    try:
        partes = re.findall(r"[\d.]+|[NSLO]", coord_str)
        lat = float(partes[0]) + float(partes[1])/60 + float(partes[2])/3600
        if partes[3] in ['S', 'O']:
            lat *= -1
        lon = float(partes[4]) + float(partes[5])/60 + float(partes[6])/3600
        if partes[7] in ['S', 'O']:
            lon *= -1
        return f"{lat},{lon}"
    except:
        return coord_str

def obter_previsao_clima(local):
    local = converter_coordenadas(local)
    config = configparser.ConfigParser()
    config.read("config.toml")
    api_key = config["weather"]["api_key"]
    if "," in local:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={local.split(',')[0]}&lon={local.split(',')[1]}&appid={api_key}&units=metric"
    else:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={local}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    forecast = []
    for item in data["list"]:
        forecast.append({
            "data": item["dt_txt"],
            "temp": item["main"]["temp"],
            "umidade": item["main"]["humidity"],
        })
    return pd.DataFrame(forecast)
