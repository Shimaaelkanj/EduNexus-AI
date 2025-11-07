# career_assistant/views.py
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Use the existing modules in this app
from .extract_cv import extract_text_from_pdf
from .skill_extractor import analyze_skills_from_cv
from .roadmap_generator import generate_roadmap
from .db_handler import save_cv_analysis  # optional: will try to save to MongoDB

def validate_jwt_token(token: str):
    """
    Validate and decode a JWT token using SimpleJWT.

    Returns:
        dict: payload data if token is valid
    Raises:
        Exception: if token is invalid or expired
    """
    try:
        access_token = AccessToken(token)
        payload = access_token.payload  # Decoded claims
        return payload
    except TokenError as e:
        raise Exception(f"❌ Invalid or expired token: {str(e)}")
    
    
class AnalyzeCV(APIView):
    def post(self, request, format=None):
        try:
            if "file" not in request.FILES:
                return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

            file_obj = request.FILES["file"]

            # Save uploaded file temporarily inside project folder
            upload_dir = os.path.join(os.getcwd(), "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file_obj.name)

            with open(file_path, "wb+") as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)

            # Use existing pipeline: extract text -> analyze skills -> generate roadmap
            # analyze_skills_from_cv expects a file path and returns dict with skills_found/missing
            analysis = analyze_skills_from_cv(file_path)
            skills_found = analysis.get("skills_found", [])
            skills_missing = analysis.get("skills_missing", [])

            roadmap = generate_roadmap(skills_missing)

            # Try saving to DB (db_handler.save_cv_analysis expects filename, skills_found, skills_missing)
            try:
                save_cv_analysis(file_obj.name, skills_found, skills_missing)
            except Exception:
                # Don't fail the whole request if DB is not available
                pass

            # Remove uploaded file after processing
            try:
                os.remove(file_path)
            except OSError:
                pass

            return Response({
                "filename": file_obj.name,
                "skills_found": skills_found,
                "skills_missing": skills_missing,
                "roadmap": roadmap
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
