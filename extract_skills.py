# extract_skills_spacy_only.py

import pdfplumber
from docx import Document
import re
import spacy
import os

# -------------------------------
# 1️⃣ دوال لاستخراج النص
# -------------------------------

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# -------------------------------
# 2️⃣ تنظيف النصوص
# -------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# -------------------------------
# 3️⃣ استخراج المهارات باستخدام Spacy (Noun chunks)
# -------------------------------

nlp = spacy.load("en_core_web_sm")

def extract_skills_spacy(text):
    doc = nlp(text)
    skills = set()
    for chunk in doc.noun_chunks:
        skills.add(chunk.text.strip())
    return list(skills)

# -------------------------------
# 4️⃣ الدالة الرئيسية
# -------------------------------

def extract_skills(file_path):
    # التحقق من نوع الملف
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise Exception("Unsupported file type! Use PDF or DOCX.")

    # تنظيف النص
    text = clean_text(text)

    # استخراج المهارات
    skills = extract_skills_spacy(text)

    return skills

# -------------------------------
# 5️⃣ مثال تشغيل
# -------------------------------

if __name__ == "__main__":
    file_path = "MyResume.pdf"  # ضع اسم ملف CV هنا
    skills = extract_skills(file_path)
    print("Extracted skills:")
    for s in skills:
        print("-", s)
