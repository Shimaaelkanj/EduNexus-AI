from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from extract_cv import extract_text_from_pdf
from skill_extractor import analyze_skills_from_cv
from db_handler import save_cv_analysis
from roadmap_generator import generate_roadmap  

class AnalyzeCV(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
      #ٌReceive the file
        file_obj = request.FILES["file"]
        with open(file_obj.name, "wb+") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        # Analyze the skills from skill_extractor
        analysis = analyze_skills_from_cv(file_obj.name)

        # Save the result in DB
        save_cv_analysis(
            analysis["filename"],
            analysis["skills_found"],
            analysis["skills_missing"]
        )

        # Generate roadmap
        roadmap = generate_roadmap(analysis["skills_missing"])

        return Response({
            "filename": analysis["filename"],
            "skills_found": analysis["skills_found"],
            "skills_missing": analysis["skills_missing"],
            "roadmap": roadmap
        })
