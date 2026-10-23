import requests
url="https://api.open-meteo.com/v1/forecast"
weather_code_map = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    97: "Heavy thunderstorm",
    99: "Thunderstorm with heavy hail"
}
params = {
    "latitude": 27.8563,
    "longitude": 112.9074,
    "current": ["temperature_2m", "apparent_temperature", "weather_code"],
    "timezone": "Asia/Shanghai"
}

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data["current"]
    code=current["weather_code"]
    weather=weather_code_map.get(code,f"未知天气{code}")

    print("湘潭雨湖区 当前天气")
    print(f"温度：{current['temperature_2m']}℃")
    print(f"体感温度：{current['apparent_temperature']}℃")
    print(f"天气状况：{weather}")
    
except requests.exceptions.RequestException as e:
    print(f"网络请求失败：{e}")
except Exception as e:
    print(f"数据解析失败：{e}")