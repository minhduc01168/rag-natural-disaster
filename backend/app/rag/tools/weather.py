import hashlib
import requests

class WeatherTool:
    """
    Công cụ gọi API Thời tiết.
    - mock=False: Sử dụng API wttr.in
    - mock=True: Sử dụng Mock data
    """
    def __init__(self, mock: bool = False):
        self.mock = mock

    def get_weather(self, location: str) -> dict:
        """
        Lấy thông tin thời tiết hiện tại của một khu vực.
        """
        if not self.mock:
            try:
                # Gọi API thực tế
                url = f"https://wttr.in/{location}?format=j1"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                current = data.get("current_condition", [{}])[0]
                
                return {
                    "location": location,
                    "temperature": f"{current.get('temp_C', 'N/A')}°C",
                    "condition": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
                    "wind_speed": f"{current.get('windspeedKmph', 'N/A')} km/h",
                    "humidity": f"{current.get('humidity', 'N/A')}%"
                }
            except Exception as e:
                print(f"Weather API Error: {e}, falling back to mock data.")

        # Fallback hoặc Mock Mode
        hash_val = int(hashlib.md5(location.encode()).hexdigest(), 16)
        
        temperatures = [22, 25, 28, 30, 32, 35, 18, 15]
        conditions = [
            "Trời nắng gắt, nguy cơ cháy rừng", 
            "Mưa to, nguy cơ ngập lụt", 
            "Trời nhiều mây, rải rác có mưa",
            "Mưa rào và dông",
            "Trời quang mây tạnh"
        ]
        wind_speeds = [5, 10, 15, 25, 40, 60]
        
        return {
            "location": location,
            "temperature": f"{temperatures[hash_val % len(temperatures)]}°C",
            "condition": conditions[hash_val % len(conditions)],
            "wind_speed": f"{wind_speeds[hash_val % len(wind_speeds)]} km/h",
            "humidity": "65%"
        }
