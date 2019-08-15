from django.urls import path,re_path
from .views import *


urlpatterns = [
   path(r'category/',CourseCategoryApiView.as_view()),
   path(r'course/',CourseApiView.as_view()),
   re_path(r'^course/(?P<pk>\d+)/',CourseDetailRetrieveAPIView.as_view())
]