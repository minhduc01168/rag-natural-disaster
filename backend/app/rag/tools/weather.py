class WeatherTool:
    """
    Công cụ gọi API Thời tiết (OpenWeatherMap / Mock).
    """
    def __init__(self, mock: bool = True):
        self.mock = mock

    def get_weather(self, location: str) -> dict:
        """
        Lấy thông tin thời tiết hiện tại của một khu vực.
        """
        if self.mock:
            # Mock data cho demo
            return {
                "location": location,
                "temperature": "28°C",
                "condition": "Mưa to, nguy cơ ngập lụt",
                "wind_speed": "15 km/h"
            }
        # Thực tế sẽ gọi API: requests.get(...)
        return {}
