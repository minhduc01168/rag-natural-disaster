class GeoTool:
    """
    Công cụ tra cứu thông tin địa lý / bản đồ rủi ro (Susceptibility Map).
    """
    def __init__(self, mock: bool = True):
        self.mock = mock

    def check_risk_zone(self, location: str) -> dict:
        """
        Kiểm tra mức độ rủi ro thiên tai của một địa điểm dựa trên tọa độ/tên.
        """
        if self.mock:
            # Mock data cho demo
            return {
                "location": location,
                "risk_level": "Cao",
                "disaster_type": "Sạt lở đất",
                "safe_zones_nearby": ["Nhà văn hóa xã", "Trường học trên đồi"]
            }
        return {}
