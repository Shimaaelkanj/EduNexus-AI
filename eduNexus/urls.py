from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path("analyze/", include('career_assistant.urls')),
    path("auth/", include('accounts.urls')),
]
