import pytest
import os
from unittest.mock import patch
from app.rag.ingestion.parser import MasterDocumentParser

@pytest.fixture
def master_parser():
    return MasterDocumentParser()

@patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
@patch('app.rag.ingestion.parser.os.path.exists', return_value=True)
@patch('app.rag.ingestion.parser.GeminiDocumentParser.parse_document')
def test_route_pdf_to_gemini(mock_gemini, mock_exists, master_parser):
    mock_gemini.return_value = "# Markdown from Gemini"
    result = master_parser.route_and_parse("test_file.pdf")
    mock_gemini.assert_called_once_with("test_file.pdf")
    assert result == "# Markdown from Gemini"

@patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
@patch('app.rag.ingestion.parser.os.path.exists', return_value=True)
@patch('app.rag.ingestion.parser.DoclingParser.parse_document')
@patch('app.rag.ingestion.parser.GeminiDocumentParser.parse_document')
def test_fallback_gemini_to_docling(mock_gemini, mock_docling, mock_exists, master_parser):
    mock_gemini.side_effect = Exception("Quota Exceeded")
    mock_docling.return_value = "# Markdown from Docling Fallback"
    result = master_parser.route_and_parse("test_file.pdf")
    mock_gemini.assert_called_once_with("test_file.pdf")
    mock_docling.assert_called_once_with("test_file.pdf")
    assert result == "# Markdown from Docling Fallback"

@patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
@patch('app.rag.ingestion.parser.os.path.exists', return_value=True)
@patch('app.rag.ingestion.parser.DoclingParser.parse_document')
def test_route_docx_to_docling(mock_docling, mock_exists, master_parser):
    mock_docling.return_value = "# Markdown from Docling"
    result = master_parser.route_and_parse("test_file.docx")
    mock_docling.assert_called_once_with("test_file.docx")
    assert result == "# Markdown from Docling"
