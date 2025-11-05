from django.urls import path, include
from core.views import (
    summarize_title,
    summarize_intro,
    summarize_professional,
    summarize_student,
    summarize_all,
)

urlpatterns = [
    path('summarize/title/', summarize_title.summarize_title_api),
    path('summarize/intro/', summarize_intro.summarize_intro_api),
    path('summarize/professional/', summarize_professional.summarize_professional_api),
    path('summarize/student/', summarize_student.summarize_student_api),
    path("summarize/all/", summarize_all.summarize_all_api),
]
