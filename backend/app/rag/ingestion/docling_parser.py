import os
from typing import Optional
from docling.document_converter import DocumentConverter

class DoclingParser:
    """
    Trình phân tích tài liệu đa định dạng (PDF, DOCX, PPTX, HTML, Image, MD) sử dụng IBM Docling.
    Có khả năng chạy Offline trên server và hỗ trợ OCR cho ảnh/PDF scan.
    """
    
    def __init__(self):
        print("Đang khởi tạo Docling DocumentConverter (có thể tốn thời gian tải model OCR lần đầu)...")
        # Khởi tạo mặc định với khả năng nhận diện bảng và cấu trúc, bao gồm cả OCR tự động
        self.converter = DocumentConverter()
        print("Đã khởi tạo DoclingParser thành công.")

    def parse_document(self, file_path: str) -> str:
        """
        Đọc file và xuất ra định dạng Markdown chuẩn xác.
        Hỗ trợ: PDF, DOCX, PPTX, Image (png, jpeg), Markdown, HTML.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

        print(f"Docling đang xử lý file: '{os.path.basename(file_path)}'...")
        try:
            # Converter xử lý tự động file type và chạy OCR nếu cần
            result = self.converter.convert(file_path)
            
            # Xuất thẳng ra Markdown
            markdown_content = result.document.export_to_markdown()
            return markdown_content
            
        except Exception as e:
            print(f"Lỗi khi xử lý bằng Docling: {e}")
            raise e
