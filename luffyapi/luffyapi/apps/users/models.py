from django.db import models
from django.contrib.auth.models import AbstractUser
from luffyapi.utils.models import BaseModel
from courses.models import Course
# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="手机号码")
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True, verbose_name="头像")
    credit = models.IntegerField(default=0, verbose_name="熊币")


    class Meta:
        db_table = 'ly_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class Credit(BaseModel):
    OPERA_OPION = (
        (1, "赚取"),
        (2, "消费"),
    )
    user=models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="用户",related_name='usercredit')
    opera = models.SmallIntegerField(choices=OPERA_OPION, verbose_name="操作类型")
    number = models.SmallIntegerField(default=0, verbose_name="积分数值")

    class Meta:
        db_table='ly_credit'
        verbose_name='积分流水'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '%s %s %s 熊币'%( self.user.username, self.OPERA_OPION[self.opera][1], self.number)


class UserCouse(BaseModel):
    pay_choices = (
        (1, '用户购买'),
        (2, '免费活动'),
        (3, '活动赠品'),
        (4, '系统赠送'),
    )
    user=models.ForeignKey(User, related_name='user_courses', on_delete=models.DO_NOTHING,verbose_name="用户")
    course=models.ForeignKey(Course, related_name='course_users', on_delete=models.DO_NOTHING, verbose_name="课程")
    trade_no=models.CharField(max_length=128, null=True,blank=True, verbose_name="支付平台的账单号")
    buy_type=models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="购买方式")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="购买时间")
    out_time = models.DateTimeField(null=True, blank=True, verbose_name="过期时间")

    class Meta:
        db_table='ly_user_course'
        verbose_name='课程购买记录'
        verbose_name_plural=verbose_name

