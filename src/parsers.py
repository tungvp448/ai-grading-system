import os
import docx
from pypdf import PdfReader

def extract_text_from_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif ext == ".docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError(f"Định dạng file '{ext}' không hỗ trợ. Sử dụng .pdf, .docx hoặc .txt")

    if not text.strip():
        raise ValueError(f"Không trích xuất được nội dung từ file: {file_path}")

    return text
