from django.shortcuts import render
from django.http import JsonResponse
from .mongo_utils import get_collection, check_mongo_connection, get_list_databases
import os
import pdfplumber
import tempfile
from docx import Document
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from transformers import pipeline

def users_list(request):
    users_col = get_collection("users")
    users = list(users_col.find({}, {"_id": 0}))
    return JsonResponse(users, safe=False)


def test_mongo(request):
    status = check_mongo_connection()

    if status:
        # Try inserting and reading back
        test_col = get_collection("test")
        test_doc = {"message": "Hello MongoDB"}
        test_col.insert_one(test_doc)

        doc = test_col.find_one({"message": "Hello MongoDB"}, {"_id": 0})
        return JsonResponse({"connected": True, "test_doc": doc})
    else:
        return JsonResponse({"connected": False})

def list_databases(request):
    dbs = get_list_databases()
    if dbs:
        return JsonResponse({"databases": dbs})
    return JsonResponse({"databases": []})

# Load HuggingFace summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# ---------- File Parsing ----------
def parse_pdf(file_path):
    content = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content += page.extract_text() + "\n"
    return content.strip()

def parse_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def parse_file(request):
    """Upload a file (PDF/DOCX) and extract text"""

    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return Response(
            {"error": "No file uploaded. Please send with key 'file'."},
            status=400
        )

    file_ext = os.path.splitext(uploaded_file.name)[1].lower()

    # Save file safely in a temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        for chunk in uploaded_file.chunks():
            tmp.write(chunk)
        file_path = tmp.name 

    try:
        if file_ext == ".pdf":
            content = parse_pdf(file_path)
        elif file_ext == ".docx":
            content = parse_docx(file_path)
        else:
            return Response(
                {"error": f"Unsupported file type '{file_ext}'"},
                status=400
            )

        return Response({
            "filename": uploaded_file.name,
            "content": content
        })

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)