from rest_framework.serializers import ModelSerializer
from .models import BannerInfo,NavInfo
class BannerInfoSerializer(ModelSerializer):
    """轮播图序列化器"""
    class Meta:
        model=BannerInfo
        fields = ("image","link")

class NavInfoSerializer(ModelSerializer):
    class Meta:
        model=NavInfo
        fields=['id','name','link']