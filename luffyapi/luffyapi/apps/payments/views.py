from rest_framework.views import  APIView
from alipay import AliPay
from order.models import Order
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from django.db import transaction
from coupon.models import UserCoupon
import logging
from users.models import  User,UserCouse,Credit
from datetime import datetime
from courses.models import CourseExpire

log=logging.getLogger('django')

class AlipayAPIView(APIView):
    def post(self,request,order_number):
        '''生成支付宝跳转的链接地址'''

        try:
            order=Order.objects.get(order_number=order_number,order_status=0)
        except Order.DoesNotExist:
            return Response({"message":"对不起当前订单不存在或者已经支付了！"}, status=status.HTTP_400_BAD_REQUEST)

    #创建支付宝的sdk对象
        alipay=AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_path=settings.ALIAPY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=settings.ALIAPY_CONFIG["alipay_public_key_path"],
            sign_type=settings.ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG["debug"],  # 默认False
        )

        #生成跳转地址(固定格式)
        order_string=alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,#订单号
            total_amount=float(order.real_price),
            subject=order.order_title,
            return_url=settings.ALIAPY_CONFIG['return_url'],
            notify_url=settings.ALIAPY_CONFIG['notify_url']
        )

        pay_url=settings.ALIAPY_CONFIG['gateway_url']+order_string

        return Response({'pay_url':pay_url})

class AlipayResultAPIView(AlipayAPIView):
    '''支付宝同步接受结果'''
    def get(self,request):

        data = request.query_params.dict()
        return self.result(data)


    def post(self,request):

        #是不是一定要用post方法?
        #代理服务器因为转发的原因,会导致支付时候出现问题,所以代理服务器不能用来使用支付功能
        data = request.data.dict()
        return self.result(data)


    def result(self,data):
        signature = data.pop("sign")

        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_path=settings.ALIAPY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=settings.ALIAPY_CONFIG["alipay_public_key_path"],
            sign_type=settings.ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG["debug"],  # 默认False
        )

        # verification
        success = alipay.verify(data, signature)

        # if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        if success:
            # 修改订单状态

            out_trade_no = data.get('out_trade_no')
            try:
                order = Order.objects.get(order_number=out_trade_no, order_status=0)
                order.pay_time=datetime.now()
            except:
                return Response({'message': '订单不存在或已被支付'}, status=status.HTTP_403_FORBIDDEN)

            with transaction.atomic():
                save_id = transaction.savepoint()
                order.order_status = 1
                order.save()
                # 处理用户的优惠券使用
                if order.coupon > 0:
                    coupon_id = order.coupon
                    try:
                        user_coupon = UserCoupon.objects.get(pk=coupon_id, is_use=False)
                        user_coupon.is_use = True
                        user_coupon.save()
                    except:
                        log.error('订单生成中优惠券有误')
                        transaction.savepoint_rollback(save_id)

                # 用户的积分处理
                # 用户积分信息的变更
                # 积分流水的添加
                if order.credit > 0:

                    user = order.user
                    user_credit = user.credit - order.credit

                    if user_credit > 0:
                        credit = Credit.objects.create(user=user, opera=2, number=order.credit, orders=0)
                        user.credit = user_credit
                        user.save()
                        credit.save()
                    else:

                        log.error('生成订单有误,积分计算出现问题')
                        transaction.savepoint_rollback(save_id)

                # 课程购买记录的处理
                order_course = order.order_courses.all()
                data_list = []
                course_list=[]
                for item in order_course:

                    # 判断购买时是否到期,是否为永久期限
                    try:
                        user_course_info = UserCouse.objects.get(user=order.user, course=item.course)
                        if datetime.now() > user_course_info.out_time:
                            start_time = datetime.now().timestamp()
                        else:
                            start_time = user_course_info.out_time.timestamp()
                    except:
                        start_time = datetime.now().timestamp()

                    try:
                        course_expire = CourseExpire.objects.get(course=item.course, expire_time=item.expire)
                        timer = item.expire * 60 * 60 * 24

                        print(datetime.fromtimestamp(start_time))

                        if datetime.fromtimestamp(start_time) != "2199-01-01 00:00:00":

                            out_time = start_time + timer
                            out_time = datetime.fromtimestamp(out_time)
                        else:
                            out_time = "2199-01-01 00:00:00"
                    except:

                        out_time = "2199-01-01 00:00:00"

                    data_list.append(
                        UserCouse(user=order.user, course=item.course, trade_no=data.get('trade_no'), buy_type=1,
                                  pay_time=order.pay_time, out_time=out_time, orders=0)

                    )

                    course_list.append(
                        item.course.name
                    )


                try:
                    UserCouse.objects.bulk_create(data_list)
                except:
                    log.error('订单%s出现购买记录写入写入错误' % order.order_number)
                    pass


                return_data = {
                    'order_number': order.order_number,
                    'pay_time': order.pay_time,
                    'real_price': order.real_price,
                    'course_list':course_list
                }
                return Response(return_data)
        else:
            return Response({'message': '支付失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

