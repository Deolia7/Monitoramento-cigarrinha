
import requests

def obter_previsao_clima():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Sao%20Paulo&appid={{your_api_key}}&units=metric"
        response = requests.get(url)
        data = response.json()
        chuva = data.get("rain", {}).get("1h", 0)
        return {"rain": chuva}
    except:
        return {}
