from rest_framework.response import Response
from .serializers import CourseCategoryModelSerializer
from rest_framework.generics import ListAPIView
from .models import CourseCategory

class CourseCategoryApiView(ListAPIView):
    queryset =CourseCategory.objects.filter(is_delete=False,is_show=True).order_by('orders')
    serializer_class = CourseCategoryModelSerializer