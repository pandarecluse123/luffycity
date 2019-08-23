from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import UserCoupon
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import UserCouponSerializer
# Create your views here.

class CouponLsitAPIView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = UserCoupon.objects.filter(is_show=True,is_delete=False,is_use=False)
    serializer_class = UserCouponSerializer
    filter_backends = [DjangoFilterBackend]
    # filter_fields=('user_id',)
    filter_fields=['user_id']