from django.urls import path
from . import views

urlpatterns = [
    path("test-mongo/", views.test_mongo, name="test_mongo"),
    path("users/", views.users_list, name="users_list"),
    path("list-databases/", views.list_databases, name="list_databases"),
    path("parse/", views.parse_file, name="parse_file"),
    path("summarize/", views.summarize_text, name="summarize_text"),
    path("outline/", views.generate_outline, name="generate_outline"),
]
