
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    # page_query_param = 'page'#设置代表页码的变量名,默认是page
    page_size = 5
    max_page_size = 10 #限制页面最多展示的条数
    # page_size_query_param = 'size'#设置调整显示条件的变量名,默认是size