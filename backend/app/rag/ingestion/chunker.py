from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

class SemanticChunker:
    """
    Chia nhỏ văn bản dựa trên cấu trúc Markdown (H1, H2, H3).
    - Giữ lại đề mục trong nội dung (strip_headers=False) để bảo toàn ngữ cảnh ngữ nghĩa.
    - Gộp các đoạn nhỏ hơn min_chunk_size để tránh tình trạng chunk bé vụn.
    - Cắt các đoạn quá dài (> chunk_size) bằng RecursiveCharacterTextSplitter.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150, min_chunk_size: int = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        if min_chunk_size is None:
            # Mặc định tối đa 250 ký tự, nhưng điều chỉnh theo tỉ lệ nếu chunk_size nhỏ trong test
            self.min_chunk_size = min(250, max(20, chunk_size // 4))
        else:
            self.min_chunk_size = min_chunk_size

        # Giới hạn thẻ Heading ở mức H1, H2, H3 để tránh xé vụn các tiểu mục/định nghĩa ngắn
        self.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on,
            strip_headers=False
        )
        
        # Splitter cho các khối vượt quá chunk_size
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def _merge_small_chunks(self, docs: List[Document]) -> List[Document]:
        """
        Gộp các đoạn tài liệu có độ dài dưới min_chunk_size vào đoạn kế tiếp (hoặc trước đó)
        để loại bỏ hoàn toàn các chunk bé vụn (20-100 ký tự).
        """
        if not docs:
            return []

        merged: List[Document] = []
        curr: Document = None

        for doc in docs:
            content = doc.page_content.strip()
            if not content:
                continue

            if curr is None:
                curr = Document(page_content=content, metadata=dict(doc.metadata or {}))
                continue

            # Nếu đoạn hiện tại chưa đạt min_chunk_size, gộp tiếp
            if len(curr.page_content) < self.min_chunk_size:
                curr.page_content = curr.page_content + "\n\n" + content
                if doc.metadata:
                    curr.metadata.update(doc.metadata)
            else:
                merged.append(curr)
                curr = Document(page_content=content, metadata=dict(doc.metadata or {}))

        if curr is not None:
            # Nếu đoạn cuối cùng còn quá nhỏ và đã có đoạn trước đó, gộp vào đoạn trước
            if merged and len(curr.page_content) < self.min_chunk_size:
                merged[-1].page_content = merged[-1].page_content + "\n\n" + curr.page_content
            else:
                merged.append(curr)

        return merged

    def chunk_text(self, markdown_text: str) -> List[Document]:
        """
        Thực hiện chunking 3 bước:
        1. Cắt theo Header Markdown (H1, H2, H3) và giữ nguyên tiêu đề trong nội dung.
        2. Gộp các đoạn bé vụn (< min_chunk_size).
        3. Cắt các khối quá dài (> chunk_size) bằng RecursiveCharacterTextSplitter.
        """
        if not markdown_text or not markdown_text.strip():
            return []
            
        # Lớp 1: Cắt theo thẻ Markdown H1-H3
        md_splits = self.markdown_splitter.split_text(markdown_text)
        
        # Lớp 2: Gộp các đoạn nhỏ bé vụn
        merged_splits = self._merge_small_chunks(md_splits)
        
        # Lớp 3: Cắt các khối vượt quá chunk_size
        final_splits = self.text_splitter.split_documents(merged_splits)
        
        # Loại bỏ các chunk rác rỗng (< 20 ký tự)
        clean_splits = [d for d in final_splits if len(d.page_content.strip()) >= 20]
        
        return clean_splits
