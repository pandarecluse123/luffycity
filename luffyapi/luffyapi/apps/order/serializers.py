from rest_framework import serializers
from .models import Order,OrderDetail
from datetime import datetime
import random
from django_redis import get_redis_connection
from courses.models import Course,CourseExpire
from django.db import transaction
from coupon.models import UserCoupon
from django.conf import  settings

class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=[   "id", "order_title", "total_price",
            "real_price", "order_number", "order_status",
            "pay_type", "credit",
            "coupon", "pay_time",
                ]
        extra_kwargs={
            "id": {"read_only": True, },
            "order_title": {"read_only": True, },
            "total_price": {"read_only": True, },
            "real_price": {"read_only": True, },
            "order_number": {"read_only": True, },
            "order_status": {"read_only": True, },
            "pay_time": {"read_only": True, },
            "pay_type": {"required": True, },
            "credit": {"required": True, "min_value": 0},
            "coupon": {"required": True, },
        }

    def create(self,validated_data):
        """生成订单"""
        """1. 先生成订单记录"""
        # 接受客户端提交的数据

        pay_type=validated_data.get('pay_type')
        credit=validated_data.get('credit',0)
        coupon=validated_data.get('coupon',0)
        #生成必要的参数
        user_id=1
        # user_id=self.context['request'].user.id#在序列化器中使用context取得request对象
        order_title='路飞学城课程购买'
        order_number=datetime.now().strftime('%Y%m%d%H%M%S')+('%06d'%user_id)+('%04d'%random.randint(0,9999))
        order_status=0


        #从redis中提取勾选商品
        redis=get_redis_connection('cart')
        course_set=redis.smembers('selected_%s'%user_id)
        cart_list=redis.hgetall('cart_%s'%user_id)

        #如果没有勾选的商品,则不能下单
        if len(course_set)<1:
            raise serializers.ValidationError('对不起,当前没有选中任何课程')

        with transaction.atomic():
        #生成订单记录
            save_id=transaction.savepoint()
            order=super().create({
                'order_title':order_title,
                'total_price':0,
                'real_price':0,
                'order_number':order_number,
                'order_status':order_status,
                'pay_type':pay_type,
                'credit':credit,
                'coupon':coupon,
                'order_desc':'',
                'user_id':user_id,
                'orders':0,
            })

            """2. 再生成订单详情"""
            # 声明订单总价格和订单实价
            total_price=0
            for course_id_bytes in course_set:
                course_expire_bytes=cart_list[course_id_bytes]
                expire_id=int(course_expire_bytes.decode())

                course_id=int(course_id_bytes.decode())

                try:
                    course=Course.objects.get(pk=course_id)
                except:
                    transaction.savepoint_rollback(save_id)
                    raise serializers.ValidationError("对不起，商品课程不存在！")

                #提取课程的有效期选项
                try:
                    course_expire=CourseExpire.objects.get(course=course,expire_time=expire_id)
                    price=course_expire.price


                except CourseExpire.DoesNotExist:
                    price=course.price



                #生成订单详情记录
                try:
                    order_detail=OrderDetail.objects.create(
                        order=order,
                        course=course,
                        expire=expire_id,
                        price=price,
                        real_price=course.real_price(price),
                        discount_name=course.discount_name,
                        orders=0,
                    )

                except:
                    transaction.savepoint_rollback(save_id)
                    raise serializers.ValidationError("对不起，订单生成失败！请联系客服工作人员！")

                total_price+=float(order_detail.real_price)



                #保存订单的总价格
                order.total_price=total_price
                order.real_price=total_price#暂时先默认总价格为实付价格

                #使用优惠券
                if coupon:
                    user_coupon=UserCoupon.objects.get(is_use=False,is_delete=False,is_show=True,pk=coupon)
                    start_time=user_coupon.start_time.timestamp()
                    now_time=datetime.now().timestamp()
                    end_time=start_time+float(user_coupon.coupon.timer)*60*60*24


                    if start_time>now_time and now_time>end_time:
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError('对不起,优惠券不可用')

                    if total_price<float(user_coupon.coupon.condition):
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError('对不起,优惠券使用未达到条件')

                    sale_num=float(user_coupon.coupon.sale[1:])
                    sale_type=user_coupon.coupon.sale[0]
                    if sale_type=='-':
                        order.real_price=total_price-sale_num
                    if sale_type=='*':
                        order.real_price=total_price*sale_num

                    if order.real_price<0:
                        order.real_price=0

                #使用积分抵扣
                if credit:
                    user_credit=self.context['request'].user.credit
                    if user_credit<credit:
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError('对不起,积分不足,请核对后提交')

                    if credit/settings.CREDIT_MONEY>order.real_price:
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError('对不起,积分使用超过限制,请核对后提交')
                    order.real_price=float('%.2f'%(order.real_price-credit/settings.CREDIT_MONEY))

                order.save()

            """3. 清除掉购物车中勾选的商品"""
            pip=redis.pipeline()
            pip.multi()
            for course_id_bytes in cart_list:
                if course_id_bytes in course_set:
                    pip.hdel('cart_%s'%user_id,course_id_bytes)
                    pip.srem('selected_%s'% user_id,course_id_bytes)
            pip.execute()

            return order