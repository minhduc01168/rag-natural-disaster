import os
import time
import google.generativeai as genai
from .docling_parser import DoclingParser

class GeminiDocumentParser:
    """
    Trình phân tích tài liệu sử dụng Google Gemini 1.5 (Pro/Flash).
    Upload nguyên bản file (PDF, Image) lên Gemini và dùng Prompt để trích xuất ra định dạng Markdown chuẩn,
    bảo toàn nguyên vẹn cấu trúc bảng biểu và đề mục.
    """
    
    def __init__(self, api_key: str = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            self.api_key = os.getenv("GEMINI_API_KEY")
            
        if not self.api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable or argument.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def parse_document(self, file_path: str) -> str:
        """
        Upload File và yêu cầu mô hình trích xuất ra Markdown.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

        print(f"Đang upload '{os.path.basename(file_path)}' lên Gemini...")
        gemini_file = genai.upload_file(path=file_path, display_name=os.path.basename(file_path))
        
        # Đợi một chút để file được active trên server của Google
        time.sleep(2)

        prompt = (
            "Bạn là một chuyên gia trích xuất tài liệu (Document Parser) xuất sắc. "
            "Nhiệm vụ của bạn là đọc toàn bộ nội dung trong file đính kèm (có thể là PDF, ảnh chụp, v.v) "
            "và trích xuất thành định dạng Markdown chuẩn xác nhất.\n\n"
            "CÁC QUY TẮC NGHIÊM NGẶT:\n"
            "1. Cấu trúc đề mục: Phải giữ nguyên các H1, H2, H3 (#, ##, ###).\n"
            "2. Bảng biểu (Tables): BẮT BUỘC phải chuyển đổi thành Markdown Table đúng hàng/cột.\n"
            "3. Làm sạch: Tự động loại bỏ header, footer, số trang lặp lại vô nghĩa ở mỗi trang.\n"
            "4. Văn bản liền mạch: Không ngắt dòng giữa câu (lỗi phổ biến khi copy từ PDF), hãy ghép chúng lại thành một đoạn hoàn chỉnh.\n"
            "5. Không bình luận: Chỉ in ra kết quả Markdown, không thêm câu chào hỏi nào khác."
        )

        print("Đang yêu cầu Gemini xử lý và trích xuất văn bản...")
        try:
            response = self.model.generate_content([gemini_file, prompt])
            extracted_text = response.text
        except Exception as e:
            print(f"Lỗi khi gọi API Gemini: {e}")
            raise e
        finally:
            # Dọn dẹp file trên cloud sau khi trích xuất xong
            try:
                genai.delete_file(gemini_file.name)
            except Exception as e:
                print(f"Cảnh báo: Không thể xóa file trên server Google: {e}")

        return extracted_text

class MasterDocumentParser:
    """
    Trình điều hướng xử lý tài liệu.
    Chiến lược: 
    - PDF, JPG, PNG -> Dùng Gemini (Tốt cho cấu trúc phức tạp và OCR ảnh).
    - DOCX, PPTX, MD, HTML -> Dùng Docling (Tốt cho cấu trúc office native).
    Fallback: Nếu Gemini lỗi, chuyển về Docling.
    """
    def __init__(self):
        self.gemini_parser = None
        self.docling_parser = None

    def _get_gemini(self):
        if not self.gemini_parser:
            self.gemini_parser = GeminiDocumentParser()
        return self.gemini_parser

    def _get_docling(self):
        if not self.docling_parser:
            self.docling_parser = DoclingParser()
        return self.docling_parser

    def route_and_parse(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        
        # Nhóm file ưu tiên Gemini
        gemini_preferred = ['.pdf', '.jpg', '.jpeg', '.png']
        
        if ext in gemini_preferred:
            print(f"Routing: Chọn Gemini cho định dạng {ext}")
            try:
                parser = self._get_gemini()
                return parser.parse_document(file_path)
            except Exception as e:
                print(f"Gemini thất bại ({e}). Fallback chuyển sang Docling...")
                parser = self._get_docling()
                return parser.parse_document(file_path)
        else:
            # Nhóm file ưu tiên Docling (docx, pptx, md, html, v.v)
            print(f"Routing: Chọn Docling cho định dạng {ext}")
            parser = self._get_docling()
            return parser.parse_document(file_path)

if __name__ == "__main__":
    # Test thử script
    master_parser = MasterDocumentParser()
    # print(master_parser.route_and_parse("sample.docx"))
