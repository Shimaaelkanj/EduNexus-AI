import io
import os
import tempfile
import pdfplumber
from docx import Document

def parse_pdf(file_path) -> str:
    content = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content += page.extract_text() + "\n"
    return content.strip()

def parse_docx(file_path) -> str:
    # python-docx expects a file-like object opened in binary
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def parse_file(filename: str) -> str:
    file_ext = os.path.splitext(filename.name)[1].lower()

    # Save file safely in a temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        for chunk in filename.chunks():
            tmp.write(chunk)
        file_path = tmp.name 

    try:
        if file_ext == ".pdf":
            content = parse_pdf(file_path)
        elif file_ext == ".docx":
            content = parse_docx(file_path)
        else:
            return {"error": f"Unsupported file type '{file_ext}'"},

        return{"filename": filename.name,"content": content}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)