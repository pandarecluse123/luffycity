from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="手机号码")
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True, verbose_name="头像")


    class Meta:
        db_table = 'ly_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name