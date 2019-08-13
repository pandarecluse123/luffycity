from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path,re_path
from .views import *


urlpatterns = [
    path(r'authorizations/', obtain_jwt_token, name='authorizations'),
    path(r'captcha/', VerifyCode.as_view()),
    re_path(r'sms/(?P<mobile>1[3-9]\d{9})/', SMSCodeAPIView.as_view()),
    path(r'',UserAPIView.as_view())
]