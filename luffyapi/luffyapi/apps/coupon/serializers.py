from rest_framework import serializers
from .models import UserCoupon,Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields=['name','coupon_type','condition','timer','sale']

class UserCouponSerializer(serializers.ModelSerializer):
    coupon=CouponSerializer()
    class Meta:
        model=UserCoupon
        fields=['id','start_time','coupon']