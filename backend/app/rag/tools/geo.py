import hashlib

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
            hash_val = int(hashlib.md5(location.encode()).hexdigest(), 16)
            
            risk_levels = ["Thấp", "Trung bình", "Cao", "Rất cao"]
            disaster_types = ["Sạt lở đất", "Ngập lụt", "Lũ quét", "Xâm nhập mặn"]
            safe_zones = [
                ["Nhà văn hóa xã", "Trường học trên đồi"],
                ["UBND Huyện", "Trung tâm y tế"],
                ["Khu tái định cư", "Trường THPT"],
                ["Tòa nhà kiên cố", "Đồn biên phòng"]
            ]
            
            return {
                "location": location,
                "risk_level": risk_levels[hash_val % len(risk_levels)],
                "disaster_type": disaster_types[hash_val % len(disaster_types)],
                "safe_zones_nearby": safe_zones[hash_val % len(safe_zones)]
            }
        return {}
