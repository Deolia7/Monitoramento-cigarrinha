
import requests
import re
import configparser

def converter_coordenadas(coordenada_str):
    match = re.match(r"(\d+)°(\d+)'(\d+(?:\.\d+)?)\\"([NS])\s+(\d+)°(\d+)'(\d+(?:\.\d+)?)\\"([EW])", coordenada_str)
    if not match:
        return None

    lat_g, lat_m, lat_s, lat_dir, lon_g, lon_m, lon_s, lon_dir = match.groups()
    lat = int(lat_g) + int(lat_m) / 60 + float(lat_s) / 3600
    lon = int(lon_g) + int(lon_m) / 60 + float(lon_s) / 3600
    if lat_dir == 'S':
        lat = -lat
    if lon_dir == 'W':
        lon = -lon
    return round(lat, 6), round(lon, 6)

def obter_previsao_clima(local):
    config = configparser.ConfigParser()
    config.read("config.toml")
    api_key = config["openweather"]["api_key"]

    # Verifica se é coordenada
    if "°" in local:
        coordenadas = converter_coordenadas(local)
        if coordenadas:
            lat, lon = coordenadas
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        else:
            return None
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={local}&appid={api_key}&units=metric"

    resposta = requests.get(url)
    if resposta.status_code != 200:
        return None

    dados = resposta.json()
    previsao = []
    for item in dados["list"]:
        previsao.append({
            "data": item["dt_txt"],
            "temperatura": item["main"]["temp"],
            "umidade": item["main"]["humidity"]
        })
    return previsao
