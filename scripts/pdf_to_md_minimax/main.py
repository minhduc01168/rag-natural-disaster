import os
import glob
import fitz  # PyMuPDF
import re
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Tải biến môi trường từ file .env (nếu có)
load_dotenv()

API_KEY = os.getenv("MINIMAX_API_KEY", "sk-UcGhGbEDNOBsmy1ZafYmf43pngeI0upIRcRGcwORuWYlWJGz")
BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.tokenrouter.com/v1")

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

def extract_text_from_pdf(pdf_path):
    """Trích xuất văn bản thô từ file PDF (dành cho file text base)."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        page_text = page.get_text().strip()
        if page_text:
            text += f"\n\n--- Page {page.number + 1} ---\n\n"
            text += page_text
    return text

def clean_markdown_response(raw_response):
    """Xóa thẻ <think> của model reasoning."""
    return re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL).strip()

def convert_text_to_markdown_for_rag(raw_text):
    """Xử lý văn bản PDF thông thường."""
    system_prompt = """Bạn là hệ thống tiền xử lý tài liệu cho RAG. 
Chỉ trả về Markdown, không giao tiếp. Giữ nguyên 100% ngữ cảnh, sửa lỗi ngắt dòng, tạo bảng Markdown nếu có."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Vui lòng chuẩn hóa văn bản PDF sau thành định dạng Markdown:\n\n{raw_text}"},
    ]

    try:
        response = client.chat.completions.create(
            model="MiniMax-M3",
            messages=messages,
            stream=False,
            extra_body={}
        )
        return clean_markdown_response(response.choices[0].message.content)
    except Exception as e:
        print(f"Lỗi API: {str(e)}")
        return ""

def process_scanned_page_with_vision(base64_image, page_num):
    """Dùng Vision API để OCR một trang PDF scan thành Markdown."""
    system_prompt = """Bạn là chuyên gia OCR tài liệu scan cho RAG.
Nhiệm vụ: Đọc ảnh và gõ lại toàn bộ chữ trong ảnh ra Markdown.
YÊU CẦU BẮT BUỘC:
1. KHÔNG thêm lời chào hay bình luận.
2. Nếu có bảng biểu, hãy vẽ lại thành bảng Markdown.
3. Nếu có tiêu đề, dùng #, ## cho phù hợp.
4. Trích xuất chính xác 100% nội dung chữ có trong hình."""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Vui lòng OCR trang số {page_num} này sang Markdown:"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]

    try:
        response = client.chat.completions.create(
            model="MiniMax-M3", 
            messages=messages,
            stream=False,
            extra_body={}
        )
        return clean_markdown_response(response.choices[0].message.content)
    except Exception as e:
        print(f"Lỗi API (Vision) trang {page_num}: {str(e)}")
        return ""

def process_scanned_pdf(pdf_path, filename):
    """Xử lý file scan bằng cách cắt từng trang thành ảnh và gọi Vision API."""
    print(f"[{filename}] Phát hiện file scan! Bắt đầu chuyển sang chế độ OCR bằng Vision API...")
    doc = fitz.open(pdf_path)
    full_markdown = []
    
    for page_num in range(len(doc)):
        print(f"[{filename}] Đang OCR trang {page_num + 1}/{len(doc)}...")
        page = doc[page_num]
        
        # Render trang PDF thành ảnh với độ phân giải đủ tốt (dpi=150)
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("jpeg")
        b64_img = base64.b64encode(img_bytes).decode("utf-8")
        
        # Gọi API OCR cho trang này
        md_page = process_scanned_page_with_vision(b64_img, page_num + 1)
        if md_page:
            full_markdown.append(f"\n\n<!-- Page {page_num + 1} -->\n\n" + md_page)
            
    return "".join(full_markdown)

def process_pdf_folder(input_folder, output_folder):
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = glob.glob(os.path.join(input_folder, "*.pdf"))
    if not pdf_files:
        print(f"Không tìm thấy PDF trong '{input_folder}'")
        return

    print(f"Tìm thấy {len(pdf_files)} file PDF cần xử lý.")

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        output_path = os.path.join(output_folder, filename.replace(".pdf", ".md"))
        
        print(f"\n[{filename}] Đang trích xuất văn bản...")
        raw_text = extract_text_from_pdf(pdf_path)
        
        md_content = ""
        # Nếu không có text -> file scan -> Dùng Vision API
        if not raw_text.strip():
            md_content = process_scanned_pdf(pdf_path, filename)
        else:
            # File PDF có text bình thường
            print(f"[{filename}] Đang gọi MiniMax-M3 để chuẩn hóa Markdown ({len(raw_text)} ký tự)...")
            md_content = convert_text_to_markdown_for_rag(raw_text)
            
        if md_content:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"[{filename}] Đã lưu thành công -> {output_path}")
        else:
            print(f"[{filename}] Xử lý thất bại.")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))
    
    INPUT_DIR = os.path.join(PROJECT_ROOT, "filtered_pdf")
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, "markdowns")
    
    process_pdf_folder(INPUT_DIR, OUTPUT_DIR)
