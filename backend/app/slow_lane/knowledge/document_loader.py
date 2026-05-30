from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


# Disaster prevention knowledge base in Vietnamese
DISASTER_KNOWLEDGE = [
    {
        "id": "flood-001",
        "category": "flood",
        "title": "Xử lý khi lũ lụt",
        "content": """
        Khi gặp lũ lụt:
        1. Di chuyển ngay đến nơi cao hơn
        2. Không đi qua vùng nước chảy xiết
        3. Nếu bị kẹt, lên tầng cao nhất
        4. Chuẩn bị đồ cấp cứu và nước uống
        5. Tắt điện và gas để tránh cháy nổ
        6. Liên hệ cứu hộ nếu cần thiết
        7. Không quay về nhà cho đến khi chính quyền thông báo an toàn
        """,
    },
    {
        "id": "landslide-001",
        "category": "landslide",
        "title": "Xử lý khi sạt lở đất",
        "content": """
        Khi gặp sạt lở đất:
        1. Di chuyển ra xa khu vực sạt lở ngay lập tức
        2. Không ở dưới chân đồi hoặc núi
        3. Nếu nghe tiếng động bất thường, chạy ngay
        4. Tìm nơi đất cứng, ổn định
        5. Nếu bị kẹt, bảo vệ đầu và hô hấp
        6. Gọi cứu hộ 113 hoặc 115
        7. Không quay lại khu vực nguy hiểm
        """,
    },
    {
        "id": "typhoon-001",
        "category": "typhoon",
        "title": "Xử lý khi bão",
        "content": """
        Khi có bão:
        1. Ở trong nhà, đóng chặt cửa sổ
        2. Tránh xa cửa kính
        3. Chuẩn bị đèn pin, nước, thức ăn
        4. Sạc đầy điện thoại
        5. Không ra ngoài khi bão đang mạnh
        6. Theo dõi tin tức thường xuyên
        7. Nếu nhà không an toàn, di trú đến nơi trú ẩn
        """,
    },
    {
        "id": "earthquake-001",
        "category": "earthquake",
        "title": "Xử lý khi động đất",
        "content": """
        Khi có động đất:
        1. Ngay lập tức: DROP, COVER, HOLD ON
        2. Ngồi xuống, trốn dưới bàn chắc chắn
        3. Giữ chặt chân bàn
        4. Tránh xa cửa kính, tủ nặng
        5. Nếu ở ngoài, tìm nơi rộng rãi
        6. Nếu ở trong thang máy, nhấn nút dừng
        7. Sau khi động đất dừng, kiểm tra thương tích
        """,
    },
    {
        "id": "cpr-001",
        "category": "first-aid",
        "title": "Hồi sức tim phổi (CPR)",
        "content": """
        Kỹ thuật CPR:
        1. Kiểm tra an toàn xung quanh
        2. Gọi cấp cứu 115
        3. Đặt nạn nhân nằm ngửa trên bề mặt cứng
        4. Đặt hai tay lên ngực, giữa hai núm vú
        5. Ép ngực 30 lần (sâu 5-6cm)
        6. Thổi ngạt 2 lần
        7. Lặp lại cho đến khi cứu thương đến
        """,
    },
    {
        "id": "bleeding-001",
        "category": "first-aid",
        "title": "Cầm máu",
        "content": """
        Cách cầm máu:
        1. Đặt nạn nhân nằm xuống
        2. Dùng vải sạch ấn mạnh vào vết thương
        3. Giữ nguyên áp lực ít nhất 15 phút
        4. Nếu máu thấm qua, đặt thêm vải bên trên
        5. Không tháo vải cũ ra
        6. Gọi cấp cứu nếu máu không ngừng
        7. Nâng cao vùng bị thương nếu có thể
        """,
    },
    {
        "id": "survival-water-001",
        "category": "survival",
        "title": "Tìm nước sạch",
        "content": """
        Cách tìm nước sạch:
        1. Tìm nguồn nước chảy (suối, sông)
        2. Thu nước mưa bằng vải sạch
        3. Đun sôi nước ít nhất 1 phút
        4. Nếu không đun được, dùng vải lọc nhiều lớp
        5. Nước từ cây: buộc túi nilon vào cành
        6. Tránh nước đọng, nước có màu lạ
        7. Nước giếng cần được kiểm tra trước khi uống
        """,
    },
    {
        "id": "survival-food-001",
        "category": "survival",
        "title": "Tìm kiếm thức ăn",
        "content": """
        Cách tìm thức ăn trong tự nhiên:
        1. Ưu tiên tìm quả chín (dâu, chuối, ổi)
        2. Kiểm tra côn trùng ăn được (dế, châu chấu)
        3. Tránh nấm màu sặc sỡ
        4. Cá và tôm là nguồn protein tốt
        5. Rau dại: thử một ít trước khi ăn nhiều
        6. Nếu không chắc, không ăn
        7. Nấu chín thức ăn khi có thể
        """,
    },
]


class DocumentLoader:
    """
    Load and manage disaster prevention documents.
    """

    def __init__(self):
        self.documents = DISASTER_KNOWLEDGE

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents."""
        return self.documents

    def get_documents_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get documents by category."""
        return [doc for doc in self.documents if doc["category"] == category]

    def get_document_by_id(self, doc_id: str) -> Dict[str, Any]:
        """Get document by ID."""
        for doc in self.documents:
            if doc["id"] == doc_id:
                return doc
        return None

    def search_documents(self, query: str) -> List[Dict[str, Any]]:
        """Search documents by keyword."""
        query_lower = query.lower()
        results = []
        for doc in self.documents:
            if (
                query_lower in doc["title"].lower()
                or query_lower in doc["content"].lower()
                or query_lower in doc["category"].lower()
            ):
                results.append(doc)
        return results

    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        return list(set(doc["category"] for doc in self.documents))


document_loader = DocumentLoader()
