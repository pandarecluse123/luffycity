from django.db.models import Q
from rest_framework.generics import ListAPIView
from .models import BannerInfo
from .serializers import BannerInfoSerializer
class BannerInfoListAPIView(ListAPIView):
    """
    轮播图列表
    """
    queryset = BannerInfo.objects.filter( Q(is_show=True) & Q(is_delete=False) ).order_by("-orders")
    serializer_class = BannerInfoSerializer