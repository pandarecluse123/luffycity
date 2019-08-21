from rest_framework.response import  Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from courses.models import Course
from django_redis import get_redis_connection
from django.conf import settings
import logging

log=logging.getLogger()

class CartCouserViewSet(ViewSet):
    # permission_classes = [IsAuthenticated]

    @action(methods=['POST'],detail=False)
    def add_course(self,request):
        course_id=request.data.get('course_id')
        user_id=request.user.id
        print(user_id)
        # user_id=1
        expire=0

        try:
            course=Course.objects.get(pk=course_id)
        except:
            return Response({'message':'对不起,商品不存在'},status=status.HTTP_403_FORBIDDEN)

        try:
            redis=get_redis_connection('cart')
            pip=redis.pipeline()
            pip.multi()

            pip.hset('cart_%s'%user_id,course_id,expire)
            pip.sadd('selected_%s'%user_id,course_id)

            pip.execute()
            total=redis.hlen('cart_%s'%user_id)
            print(total)
        except:
            log.error('redis服务器出错')
            return Response({'message':'添加购物车出现错误,请联系管理员'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message':'添加成功','total':total},status=status.HTTP_200_OK)

    @action(methods=['GET'],detail=False)
    def get_course(self,request):

        # user_id=request.user.id

        user_id=1
        data=[]
        redis=get_redis_connection('cart')
        course_list=redis.hgetall('cart_%s'%user_id)
        for course_bys in course_list:
            expire_bys=redis.hget('cart_%s'%user_id,course_bys)
            selected_list=redis.smembers('selected_%s'%user_id)

            try:
                course=Course.objects.get(pk=course_bys.decode())
                data.append({
                    'id':course.id,
                    'name':course.name,
                    'price':course.real_price(),
                    'select':True if course_bys in selected_list else False,
                    'image':settings.DOMAL_IMAGE_URL+course.course_img.url,
                    'expire_list':course.expire_list,
                })
            except:
                pass


        return Response(data)

    @action(methods=['patch'],detail=False)
    def patch(self,request):
        course_id=request.data.get('course_id')
        user_id=request.user.id
        selected=request.data.get('selected')

        redis=get_redis_connection('cart')
        try:
            if not selected:
                redis.srem('selected_%s'%user_id,course_id)
            else:
                redis.sadd('selected_%s'%user_id,course_id)
        except:
            return Response({'message':'数据库操作有误'},status=status.HTTP_403_FORBIDDEN)

        return Response({'状态勾选成功'},status=status.HTTP_200_OK)

    @action(methods=['delete'],detail=False)
    def delete(self,request):
        user_id = request.user.id
        course_id=request.query_params.get('course_id')
        try:
            redis=get_redis_connection('cart')
            pip=redis.pipeline()
            pip.multi()
            pip.hdel('cart_%s'%user_id,course_id)
            pip.srem('selected_%s'%user_id,course_id)
            pip.execute()
        except:
            print('错误')
            return Response({'message':"购物车删除错误,请联系客服"},status=status.HTTP_403_FORBIDDEN)

        return Response({'message':"删除成功"},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=False)
    def put(self,request):
        expire=request.data.get('expire')
        user_id=request.user.id
        # user_id=1
        course_id=request.data.get('course_id')
        print(course_id)
        try:
            redis=get_redis_connection('cart')
            redis.hset('cart_%s'%user_id,course_id,expire)
        except:
            return Response({'message': "更改期限错误,请联系管理员"}, status=status.HTTP_403_FORBIDDEN)

        return Response({'message':"更改成功"},status=status.HTTP_200_OK)

    @action(methods=['get'],detail=False)
    def selected_order(self,request):
        # user_id=request.user.id
        user_id=1
        redis=get_redis_connection('cart')

        selected_list=redis.smembers('selected_%s'%user_id)
        if len(selected_list)<1:
            return Response({'message': "更改期限错误,请联系管理员"}, status=status.HTTP_403_FORBIDDEN)
        data=[]

        for course_id_bys in selected_list:
            expire_time=redis.hget('cart_%s'%user_id,course_id_bys).decode()

            try:
                course=Course.objects.get(is_delete=False,pk=course_id_bys.decode())

                for i in course.expire_list:
                    print(i)
                    if i.get('expire_time')==int(expire_time):
                        expire_text=i.get('expire_text')
                        price=i.get('price')

                data.append({
                    'id':course.id,
                    'name':course.name,
                    'price':price,
                    'real_price':course.real_price(price),
                    'expire':expire_text,
                    'img':settings.DOMAL_IMAGE_URL+course.course_img.url,
                    'discount_name':course.discount_name
                })
            except:
                pass
        return Response(data)