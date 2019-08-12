from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from .views import *


urlpatterns = [
    path(r'authorizations/', obtain_jwt_token, name='authorizations'),
    path(r'captcha/', VerifyCode.as_view()),
    path(r'', UserAPIView.as_view() ),
]