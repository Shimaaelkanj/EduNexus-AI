# core/views/summarize_all_api.py
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
import asyncio, os, tempfile
from core.utils.file_reader import extract_text_from_file
from core.utils.chunking import chunk_text
from core.utils.summarizer_core import async_summarize
from core.utils.db_saver import save_summary_to_db


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def summarize_all_api(request):
    """
    Unified endpoint that summarizes text or uploaded file (PDF, DOCX, TXT)
    Returns title, intro, professional, and student-friendly summaries.
    """
    try:
        text = request.data.get("text", "").strip()
        uploaded_file = request.FILES.get("file")

        # --- Extract text from file if uploaded ---
        if not text and uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            text = extract_text_from_file(tmp_path)
            os.remove(tmp_path)

        if not text:
            return Response({"error": "No text or file provided."}, status=400)

        # --- Run async summarization pipeline ---
        async def generate_all():
            chunks = chunk_text(text, 400)
            chunk_tasks = [
                async_summarize(
                    f"Summarize the following text formally and clearly:\n\n{chunk}",
                    max_length=250,
                    min_length=120,
                )
                for chunk in chunks
            ]
            chunk_summaries = await asyncio.gather(*chunk_tasks)
            combined = " ".join(filter(None, chunk_summaries)).strip()

            title_prompt = f"Generate a short, factual title (max 10 words):\n\n{combined}"
            intro_prompt = f"Write a short 2–3 sentence introduction explaining the context:\n\n{combined}"
            professional_prompt = f"Refine this into a professional, detailed summary:\n\n{combined}"
            student_prompt = f"Rewrite this for students aged 14–18 in simple, clear language:\n\n{combined}"

            title_task = async_summarize(title_prompt, 25, 5)
            intro_task = async_summarize(intro_prompt, 100, 40)
            pro_task = async_summarize(professional_prompt, 250, 120)
            student_task = async_summarize(student_prompt, 200, 80)

            title, intro, professional, student = await asyncio.gather(
                title_task, intro_task, pro_task, student_task
            )

            return {
                "title": title or "Untitled",
                "introduction": intro,
                "professional_summary": professional,
                "student_friendly_summary": student,
            }

        result = asyncio.run(generate_all())

        # --- Save to MongoDB ---
        save_summary_to_db({
            "original_text": text[:1000],  # limit stored size
            "title": result["title"],
            "introduction": result["introduction"],
            "professional_summary": result["professional_summary"],
            "student_summary": result["student_friendly_summary"],
        })

        return Response(result, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": f"Summarization failed: {str(e)}"}, status=500)
