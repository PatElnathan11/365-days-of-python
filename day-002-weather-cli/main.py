import requests

CITIES = {
    "1": {"name": "Jakarta", "lat": -6.2088, "lon": 106.8456},
    "2": {"name": "Bekasi", "lat": -6.2383, "lon": 106.9756},
    "3": {"name": "Bandung", "lat": -6.9175, "lon": 107.6191},
    "4": {"name": "Surabaya", "lat": -7.2575, "lon": 112.7521},
    "5": {"name": "Yogyakarta", "lat": -7.7956, "lon": 110.3695},
}

def get_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current_weather", {})
        temp = current.get("temperature")
        wind_speed = current.get("windspeed")
        time_str = current.get("time")
        
        return {
            "temperature": temp,
            "wind_speed": wind_speed,
            "time": time_str
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def main():
    print("====================================")
    print("WEATHER CLI APP")
    print("====================================")
    print("Pilih kota:")
    for key, city in CITIES.items():
        print(f" [{key}] {city['name']}")
    
    choice = input("\nMasukkan nomor pilihan (1-5): ").strip()
    
    if choice in CITIES:
        selected_city = CITIES[choice]
        print(f"\n🔍 Mengambil data cuaca untuk {selected_city['name']}...")
        
        weather = get_weather(selected_city['lat'], selected_city['lon'])
        
        if weather:
            print("\n------------------------------------")
            print(f" Kota        : {selected_city['name']}")
            print(f" Suhu        : {weather['temperature']} °C")
            print(f" Kecepatan Angin: {weather['wind_speed']} km/h")
            print(f" Waktu Data  : {weather['time']}")
            print("------------------------------------")
    else:
        print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()