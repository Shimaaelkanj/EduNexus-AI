from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test-mongo/", views.test_mongo, name="test_mongo"),
    path("list-databases/", views.list_databases, name="list_databases"),
]
