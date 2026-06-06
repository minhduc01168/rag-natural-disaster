from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

class SemanticChunker:
    """
    Chia nhỏ văn bản dựa trên cấu trúc Markdown (H1, H2, H3).
    Bảo toàn ngữ nghĩa của từng đoạn bằng cách giữ lại thông tin tiêu đề trong metadata.
    """
    def __init__(self, chunk_size=1000, chunk_overlap=150):
        # Thiết lập các thẻ Heading cần tách
        self.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
        ]
        self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=self.headers_to_split_on)
        
        # Splitter dự phòng cho các đoạn văn quá dài bên trong một heading
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk_text(self, markdown_text: str):
        """
        Thực hiện chunking 2 lớp:
        1. Cắt theo Header (Markdown)
        2. Nếu một section quá dài, cắt tiếp bằng RecursiveCharacterTextSplitter
        """
        if not markdown_text or not markdown_text.strip():
            return []
            
        # Lớp 1: Cắt theo thẻ Markdown
        md_splits = self.markdown_splitter.split_text(markdown_text)
        
        # Lớp 2: Cắt các khối quá dài
        final_splits = self.text_splitter.split_documents(md_splits)
        
        return final_splits
