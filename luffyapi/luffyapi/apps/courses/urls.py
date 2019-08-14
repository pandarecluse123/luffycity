from django.urls import path,re_path
from .views import *


urlpatterns = [
   path(r'category/',CourseCategoryApiView.as_view()),
   path(r'course/',CourseApiView.as_view())
]