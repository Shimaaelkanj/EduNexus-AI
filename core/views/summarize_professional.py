# core/views/summarize_professional_api.py
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
import asyncio, os, tempfile
from core.utils.file_reader import extract_text_from_file
from core.utils.chunking import chunk_text
from core.utils.summarizer_core import async_summarize
from core.utils.db_saver import save_summary_to_db


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def summarize_professional_api(request):
    """
    Generate a detailed professional summary from raw text or uploaded file.
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

        async def summarize_chunks():
            chunks = chunk_text(text, 400)
            tasks = [
                async_summarize(
                    f"Summarize the following content in a formal, detailed, and coherent manner:\n\n{chunk}",
                    max_length=250,
                    min_length=120,
                )
                for chunk in chunks
            ]
            results = await asyncio.gather(*tasks)
            return " ".join(filter(None, results)).strip()

        professional_summary = asyncio.run(summarize_chunks())
        save_summary_to_db({"original_text": text[:1000], "professional_summary": professional_summary})

        return Response({"professional_summary": professional_summary}, status=200)

    except Exception as e:
        import traceback; traceback.print_exc()
        return Response({"error": str(e)}, status=500)
