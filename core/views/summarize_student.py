# core/views/summarize_student_api.py
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
import asyncio, os, tempfile
from core.utils.file_reader import extract_text_from_file
from core.utils.summarizer_core import async_summarize
from core.utils.db_saver import save_summary_to_db


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def summarize_student_api(request):
    """
    Generate a student-friendly simplified summary from text or file.
    """
    try:
        text = request.data.get("text", "").strip()
        uploaded_file = request.FILES.get("file")

        if not text and uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            text = extract_text_from_file(tmp_path)
            os.remove(tmp_path)

        if not text:
            return Response({"error": "No text or file provided"}, status=400)

        prompt = (
            "Rewrite the following text in simple, clear language suitable for students "
            "aged 14–18. Use short sentences and avoid complex terms:\n\n"
            f"{text}"
        )

        student_summary = asyncio.run(async_summarize(prompt, max_length=200, min_length=80))
        save_summary_to_db({"original_text": text[:1000], "student_summary": student_summary})

        return Response({"student_friendly_summary": student_summary}, status=200)

    except Exception as e:
        import traceback; traceback.print_exc()
        return Response({"error": str(e)}, status=500)
