from rest_framework.response import Response
from .serializers import CourseCategoryModelSerializer,CourseModelSerializer,CourseDetailModelSerializer
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .models import CourseCategory,Course
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .pagenations import CustomPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from luffyapi.libs.polyv import PolyvPlayer

class CourseCategoryApiView(ListAPIView):
    queryset =CourseCategory.objects.filter(is_delete=False,is_show=True).order_by('orders')
    serializer_class = CourseCategoryModelSerializer

class CourseApiView(ListAPIView):
    # queryset=Course.objects.all()
    queryset =Course.objects.filter(is_delete=False,is_show=True).order_by('orders')
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filter_fields=['course_category']
    ordering_fields=['id','students','price']
    pagination_class = CustomPagination

class CourseDetailRetrieveAPIView(RetrieveAPIView):
    queryset=Course.objects.filter(is_show=True,is_delete=False)
    serializer_class = CourseDetailModelSerializer


class PolyvAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        vid=request.query_params.get('vid')#视频播放id
        remote_addr=request.META.get('REMOTE_ADDR')#用户的ip
        user_id=request.user.id
        user_name=request.user.username
        polyv = PolyvPlayer(
            settings.POLYV_CONFIG["userId"],
            settings.POLYV_CONFIG["secretkey"],
            settings.POLYV_CONFIG["tokenUrl"],
        )
        data=polyv.get_video_token(vid,remote_addr,user_id,user_name)

        return Response(data)
