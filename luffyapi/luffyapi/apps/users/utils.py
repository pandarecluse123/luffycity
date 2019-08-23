from django.conf import settings

def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        'credit':user.credit,
        'credit_to_money':settings.CREDIT_MONEY
    }


from django.contrib.auth.backends import ModelBackend
from .models  import User
from django.db.models import Q

class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.filter(Q(username=username) | Q(mobile=username) | Q(email=username)).first()
        except User.DoesNotExist:
            return None
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
