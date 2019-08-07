from django.db.models import Q
from rest_framework.generics import ListAPIView
from .models import BannerInfo,NavInfo
from .serializers import BannerInfoSerializer,NavInfoSerializer
class BannerInfoListAPIView(ListAPIView):
    """
    轮播图列表
    """
    queryset = BannerInfo.objects.filter( Q(is_show=True) & Q(is_delete=False) ).order_by("-orders")
    serializer_class = BannerInfoSerializer

class HeaderNavListAPIView(ListAPIView):
    queryset = NavInfo.objects.filter(is_show=True,is_delete=False,opt=1).order_by("orders")
    serializer_class = NavInfoSerializer

class FooterNavListAPIView(ListAPIView):
    queryset=NavInfo.objects.filter(is_show=True,is_delete=False,opt=2).order_by("orders")
    serializer_class = NavInfoSerializer