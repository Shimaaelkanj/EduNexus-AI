import re
import io
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract
import json

def pdf(file_path):
    #Extract text from pdf
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def docs(file_path):
    #Extract text from world
    doc = Document(file_path)
    text = ""
    for parag in doc.paragraphs:
        text += parag.text + "\n"
    return text


def texts(file_path):
    #Extract text from text file
    with open(file_path, "r", encoding="utf-8" ) as f:
        return f.read()


def Cv_type(file_path):
    #Analyze the type of CV_file
    if file_path.endswith(".pdf"):
        text = pdf(file_path)
    elif file_path.endswith(".docx"):
        text = docs(file_path)
    elif file_path.endswith(".txt"):
        text = texts(file_path)
    else:
        raise ValueError("Invalid file type")
    #Print Info about the Cv
    result = {
       "filename": file_path,
        "Cv_preview": text[:]
   }
    return result


   
if __name__ == "__main__":
    path = "MyResume.pdf"
    output = Cv_type(path)
    print(json.dumps(output, indent =2, ensure_ascii=False))