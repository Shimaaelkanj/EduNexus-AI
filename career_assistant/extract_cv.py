"""extract_cv.py
Simple utilities to extract text from CV files (pdf, docx, txt).
The functions are intentionally straightforward and easy to explain.
"""
import re
import io
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file_path):
    """Return the text content of a PDF file.
    If a page has no extractable text, we append an empty string for that page.
    This function keeps a simple behavior to stay robust in tests.
    """
    text_parts = []
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                else:
                    # Page had no direct text (image-only). Put placeholder.
                    text_parts.append("")
    except FileNotFoundError:
        raise
    except Exception as e:
        # Keep errors clear for debugging in a simple format.
        raise RuntimeError(f"Failed to read PDF {file_path}: {e}")
    return "\n".join(text_parts)


def extract_text_from_docx(file_path):
    """Return concatenated text from a .docx file's paragraphs."""
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])


def extract_text_from_txt(file_path):
    """Return the content of a plain text file (UTF-8)."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_email(text):
    """Return the first email found in text or None."""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text):
    """Return the first phone-like string found or None."""
    pattern = r"(\\+?\\d{1,3}[-.\\s]?)?(\\(?\\d{2,4}\\)?[-.\\s]?)?\\d{6,10}"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def analyze_cv(file_path):
    """High-level helper: pick extractor by file extension and return basic info."""
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        text = extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format: " + file_path)

    email = extract_email(text)
    phone = extract_phone(text)

    return {
        "filename": file_path,
        "email": email,
        "phone": phone,
        "text_preview": text[:500]
    }


if __name__ == "__main__":
    # Quick local run for manual checks
    path = "MyResume.pdf"
    output = analyze_cv(path)
    import json as _json
    print(_json.dumps(output, indent=2, ensure_ascii=False))
