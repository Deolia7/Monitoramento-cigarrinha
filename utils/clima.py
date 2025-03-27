import requests
import pandas as pd
import re
from configparser import ConfigParser
from datetime import datetime, timedelta

def converter_coordenadas(coordenada):
    match = re.match(r"(\d{1,3})°(\d{1,2})'(\d{1,2}\.\d+)\"([NS]),\s*(\d{1,3})°(\d{1,2})'(\d{1,2}\.\d+)\"([EW])", coordenada)
    if not match:
        return None, None

    lat_g, lat_m, lat_s, lat_dir, lon_g, lon_m, lon_s, lon_dir = match.groups()

    lat = int(lat_g) + int(lat_m) / 60 + float(lat_s) / 3600
    lon = int(lon_g) + int(lon_m) / 60 + float(lon_s) / 3600

    if lat_dir == 'S':
        lat = -lat
    if lon_dir == 'W':
        lon = -lon

    return lat, lon

def obter_previsao_clima(local):
    config = ConfigParser()
    config.read("config.toml")
    api_key = config.get("openweather", "api_key", fallback=None)

    if not api_key:
        raise ValueError("API key do OpenWeather não encontrada no config.toml")

    if re.match(r"^-?\d+\.\d+,-?\d+\.\d+$", local):
        lat, lon = local.split(",")
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    elif "°" in local:
        lat, lon = converter_coordenadas(local)
        if lat is None or lon is None:
            raise ValueError("Coordenadas inválidas.")
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={local}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    previsoes = []
    for item in data["list"]:
        datahora = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
        if datahora.hour == 12:
            previsoes.append({
                "data": datahora.date(),
                "temp": item["main"]["temp"],
                "umidade": item["main"]["humidity"]
            })

    df = pd.DataFrame(previsoes)
    return df