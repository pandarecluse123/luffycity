from rest_framework.views import APIView
from luffyapi.libs.geetest import GeetestLib
from rest_framework.response import Response
from django.conf import settings
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserModelSerializer
from django_redis import get_redis_connection
import random
from luffyapi.utils.yuntongxun.sms import CCP
from rest_framework import status


class VerifyCode(APIView):
    #生成验证的流水号和状态
    def get(self,request):
        gt = GeetestLib(settings.PC_GEETEST_ID, settings.PC_GEETEST_KEY)
        status = gt.pre_process(settings.PC_GEETEST_USER_ID)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self,request):
        #二次验证
        gt = GeetestLib(settings.PC_GEETEST_ID, settings.PC_GEETEST_KEY)
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')
        result = gt.success_validate(challenge, validate, seccode, settings.PC_GEETEST_USER_ID)
        if not result:
            result = gt.failback_validate(challenge, validate, seccode)

        return Response({'stadus':result})


class UserAPIView(CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserModelSerializer

class SMSCodeAPIView(APIView):
    def get(self,request,mobile):
        try:
            User.objects.get(mobile=mobile)
            return Response({"message": "对不起，当前手机号已经被注册"},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        redis=get_redis_connection('sms_code')
        interval=redis.get('exp_%s'%mobile)
        if interval:
            return Response({"message": "发送间隔时间太短"}, status=status.HTTP_403_FORBIDDEN)
        sms_code="%06d"%random.randint(0,999999)

        redis.setex('sms_%s'%mobile,settings.SMS_EXPIRE_TIME,sms_code)
        redis.setex('exp_%s'%mobile,settings.SMS_INTERVAL_TIME,'_')

        ccp=CCP()
        result=ccp.send_template_sms(mobile,[sms_code,settings.SMS_EXPIRE_TIME//60],settings.SMS_TEIMPLATE_ID)
        print(result)
        if result==-1:
            return Response({"message": "短信发送失败！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "短信发送成功！"}, status=status.HTTP_200_OK)