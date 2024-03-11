from django.urls import path
from .views import upload_resume


urlpatterns = [
path('upload_video/', upload_resume, name = "upload_video")
]