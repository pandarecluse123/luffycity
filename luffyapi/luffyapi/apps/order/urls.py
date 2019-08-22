from django.urls import path
from . import views

urlpatterns=[
    path(r'',views.OrderCreateAPIView.as_view())
]