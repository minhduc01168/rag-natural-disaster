import os
import pytest
from unittest.mock import patch, MagicMock
from app.rag.ingestion.parser import GeminiDocumentParser

@pytest.fixture
def mock_gemini():
    with patch("app.rag.ingestion.parser.genai") as mock_genai:
        # Giả lập file trả về sau khi upload
        mock_file = MagicMock()
        mock_file.name = "files/mock-12345"
        mock_genai.upload_file.return_value = mock_file
        
        # Giả lập kết quả trả về từ Gemini
        mock_response = MagicMock()
        mock_response.text = "# Hướng dẫn Sinh tồn\n\nĐây là nội dung Markdown giả lập."
        
        # Giả lập GenerativeModel
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        yield mock_genai

def test_gemini_parser_init_without_key():
    # Xóa API key nếu có để test báo lỗi
    if "GOOGLE_API_KEY" in os.environ:
        del os.environ["GOOGLE_API_KEY"]
    with pytest.raises(ValueError):
        GeminiDocumentParser()

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_gemini_parser_init(mock_model, mock_configure):
    os.environ["GEMINI_API_KEY"] = "fake_key"
    parser = GeminiDocumentParser(model_name="gemini-test")
    
    mock_configure.assert_called_once_with(api_key="fake_key")

def test_parse_pdf_file_not_found():
    parser = GeminiDocumentParser(api_key="fake-key")
    with pytest.raises(FileNotFoundError):
        parser.parse_document("non_existent_file.pdf")

def test_parse_pdf_success(mock_gemini, tmp_path):
    # Tạo một file giả để test
    fake_pdf = tmp_path / "fake.pdf"
    fake_pdf.write_text("dummy content")
    
    parser = GeminiDocumentParser(api_key="fake-key")
    result = parser.parse_document(str(fake_pdf))
    
    assert "Hướng dẫn Sinh tồn" in result
    assert "Markdown giả lập" in result
    
    # Đảm bảo các hàm API của Google đã được gọi
    mock_gemini.upload_file.assert_called_once()
    mock_gemini.delete_file.assert_called_once()
