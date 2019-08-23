
from django.urls import path
from . import views

urlpatterns=[
    path(r'list/',views.CouponLsitAPIView.as_view())
]