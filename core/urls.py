# from django.urls import path
# from . import views

# urlpatterns = [
#     # path("test-mongo/", views.test_mongo, name="test_mongo"),
#     # path("users/", views.users_list, name="users_list"),
#     # path("list-databases/", views.list_databases, name="list_databases"),
#     # path("parse/", views.parse_file_api, name="parse_file"),
#     # path("summarize/", views.summarize_text_api, name="summarize_text"),
#     # path("outline/", views.generate_outline_api, name="generate_outline"),
#     path('upload/', views.upload_and_extract, name='upload_and_extract'),
#     path('summarize/', views.summarize, name='summarize'),
#     path('lessons/<str:lesson_id>/', views.lesson_detail, name='lesson_detail'),
# ]

from django.urls import path
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
