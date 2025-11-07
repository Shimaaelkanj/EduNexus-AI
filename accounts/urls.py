from django.urls import path
from core import views
from .views import RegisterView, LoginView, LessonView,ProfileView
# from .views import UploadView, AnalyzeCVView, RoadmapView, ExportPDFView, ExportDOCXView, ExportPPTXView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    #path("login/", LoginView.as_view(), name="login"),
    #path("lessons/", LessonView.as_view(), name="lessons"),
    # path("upload/", FileUploadView.as_view(), name="upload"),
    # path("upload/", UploadFileView.as_view()),
    # path("analyze_cv/", AnalyzeCVView.as_view()),
    # path("roadmap/<str:filename>/", RoadmapView.as_view()),
    # path("export/pdf/", ExportPDFView.as_view()),
    # path("export/docx/", ExportDOCXView.as_view()),
    # path("export/pptx/", ExportPPTXView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile")

]





#C:\Users\chima\AppData\Local\Programs\Python\Python312\python.exe --venv venv
#.\venv\Scripts\activate
#pip install -r requirements.txt

#asgiref                       3.5.2
#Django                        3.2.25
#djangorestframework           3.14.0
#djangorestframework-simplejwt 5.3.1
#djongo                        1.3.6
#dnspython                     2.8.0
#fpdf                          1.7.2
#lxml                          6.0.2
#pillow                        11.3.0
#pip                           25.0.1
#PyJWT                         2.10.1
#pymongo                       4.9.1
#python-docx                   1.2.0
#python-pptx                   1.0.2
#pytz                          2025.2
#sqlparse                      0.2.4
#typing_extensions             4.15.0
#tzdata                        2025.2
#xlsxwriter                    3.2.9
