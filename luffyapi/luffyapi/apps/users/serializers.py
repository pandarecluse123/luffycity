from rest_framework import serializers
from .models import User

class UserModelSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(write_only=True, max_length=6, help_text="短信验证码")
    token = serializers.CharField(max_length=1024, read_only=True, help_text="jwt的token字符串")
    class Meta():
        model=User
        fields=["id", "mobile", "password", "sms_code", "token"]
        extra_kwargs={
            "id":{
                'read_only':True
            },
            'mobile':{
                "max_length": 15,
                "required": True
            },
            'password':{
                "write_only": True,
                "max_length": 128,
                "required": True
            },
        }

    def create(self, validated_data):
        #删除多余的字段
        del validated_data['sms_code']

        #设置默认的字段
        validated_data["username"] = validated_data["mobile"]
        #调用当前模型序列化器的create
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()


        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)

        # 最终token作为user模型的一个字段返回给客户端
        user.token = jwt_encode_handler(payload)

        return user