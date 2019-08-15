from rest_framework.response import Response
from .serializers import CourseCategoryModelSerializer,CourseModelSerializer,CourseDetailModelSerializer
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .models import CourseCategory,Course
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .pagenations import CustomPagination

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


