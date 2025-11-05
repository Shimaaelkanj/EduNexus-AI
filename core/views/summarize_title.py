from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
import asyncio, os, tempfile
from core.utils.file_reader import extract_text_from_file
from core.utils.summarizer_core import async_summarize
from core.utils.db_saver import save_summary_to_db
from accounts.views import validate_jwt_token
from django.http import JsonResponse


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def summarize_title_api(request):
    """
    Unified endpoint that summarizes text or uploaded file (PDF, DOCX, TXT)
    Returns title, intro, professional, and student-friendly summaries.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    try:
        user_data = validate_jwt_token(token)
        
        print("Decoded token payload:", user_data)
        """
        Generate a concise, factual title from raw text or uploaded file.
        """
        try:
            text = request.data.get("text", "").strip()
            uploaded_file = request.FILES.get("file")

            # Extract text if a file was uploaded
            if not text and uploaded_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    for chunk in uploaded_file.chunks():
                        tmp.write(chunk)
                    tmp_path = tmp.name
                text = extract_text_from_file(tmp_path)
                os.remove(tmp_path)

            if not text:
                return Response({"error": "No text or file provided"}, status=400)

            prompt = f"Generate a concise, factual, and engaging title (max 10 words):\n\n{text}"
            title = asyncio.run(async_summarize(prompt, max_length=20, min_length=5))

            save_summary_to_db({"original_text": text[:1000], "title": title})
            return Response({"title": title or "Untitled"}, status=200)

        except Exception as e:
            import traceback; traceback.print_exc()
            return Response({"error": str(e)}, status=500)

    except Exception as e:
        # Handle invalid or expired token
        return JsonResponse({"error": str(e)}, status=401)