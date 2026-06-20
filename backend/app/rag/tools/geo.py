import hashlib
from app.db.session import SessionLocal
from sqlalchemy import text

class GeoTool:
    """
    Công cụ tra cứu thông tin địa lý / bản đồ rủi ro (Susceptibility Map).
    Kết nối trực tiếp vào PostGIS / PostgreSQL.
    """
    def __init__(self, mock: bool = False):
        self.mock = mock

    def check_risk_zone(self, location: str) -> dict:
        """
        Kiểm tra mức độ rủi ro thiên tai của một địa điểm dựa trên CSDL thực tế.
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
            
        # Truy vấn dữ liệu thực tế từ Database
        db = SessionLocal()
        try:
            # Tìm kiếm các features trong bảng spatial_features có chứa tên địa điểm
            # Giả định properties có trường 'name' hoặc 'area'
            query = text("""
                SELECT properties 
                FROM spatial_features 
                WHERE properties->>'name' ILIKE :loc 
                   OR properties->>'area' ILIKE :loc
                LIMIT 1
            """)
            result = db.execute(query, {"loc": f"%{location}%"}).fetchone()
            
            if result:
                props = result[0]
                return {
                    "location": props.get("name") or props.get("area") or location,
                    "risk_level": props.get("risk_level", "Chưa đánh giá"),
                    "disaster_type": props.get("disaster_type", "Sạt lở đất"),
                    "safe_zones_nearby": ["Khu vực an toàn được chỉ định bởi chính quyền"]
                }
            else:
                return {
                    "location": location,
                    "risk_level": "Chưa có dữ liệu khảo sát",
                    "disaster_type": "Chưa rõ",
                    "safe_zones_nearby": []
                }
        except Exception as e:
            print(f"Error querying GeoTool: {e}")
            return {
                "location": location,
                "risk_level": "Lỗi truy xuất",
                "disaster_type": "Lỗi truy xuất",
                "safe_zones_nearby": []
            }
        finally:
            db.close()

