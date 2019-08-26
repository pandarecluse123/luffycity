from django.db import models
from luffyapi.utils.models import BaseModel
from users.models import User
from courses.models import Course,CourseExpire

# Create your models here.

class Order(BaseModel):
    status_choices=(
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '超时取消'),
    )
    pay_choices=(
        (1, '支付宝'),
        (2, '微信支付'),
    )
    order_title=models.CharField(max_length=150,verbose_name="订单标题")
    total_price=models.DecimalField(max_digits=6, decimal_places=2, verbose_name="订单总价", default=0)
    real_price= models.DecimalField(max_digits=6, decimal_places=2, verbose_name="实付金额", default=0)
    order_number= models.CharField(max_length=64,verbose_name="订单号")
    order_status=models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
    pay_type= models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="支付方式")
    credit=models.IntegerField(default=0, verbose_name="使用的积分数量")
    coupon=models.IntegerField(default=0, verbose_name="用户优惠券ID")
    order_desc=models.TextField(max_length=500, verbose_name="订单描述")
    pay_time=models.DateTimeField(null=True, verbose_name="支付时间")
    user=models.ForeignKey(User, related_name='user_orders', on_delete=models.DO_NOTHING,verbose_name="下单用户")

    class Meta:
        db_table='ly_order'
        verbose_name='订单记录'
        verbose_name_plural=verbose_name


    def order_status_info(self):
        for num,info in self.status_choices:
            if num==self.order_status:
                return info

    def order_course_list(self):
        data_list=[]
        course_list=self.order_courses.all()

        for item in course_list:
            try:
                expire=CourseExpire.objects.get(course=item.course,expire_time=item.expire)
                expire_text=expire.expire_text
            except:
                if item.expire==0:
                    expire_text='永久有效'
                else:
                    raise CourseExpire.DoesNotExist

            data_list.append(
                {
                    'name':item.course.name,
                    'expire':expire_text,
                    'price':item.price,
                    'real_price':item.real_price,
                    'discount_name':item.discount_name,
                    # 'viedo_url':item.course.course_video.url
                }
            )

        return data_list



    def __str__(self):
        return "%s,总价: %s,实付: %s" % (self.order_title, self.total_price, self.real_price)

class OrderDetail(BaseModel):
    order=models.ForeignKey(Order, related_name='order_courses', on_delete=models.CASCADE, verbose_name="订单")
    course= models.ForeignKey(Course, related_name='course_orders', on_delete=models.CASCADE, verbose_name="课程")
    expire = models.IntegerField(default='0', verbose_name="有效期周期")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价")
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程实价")
    discount_name = models.CharField(max_length=120, null=True, default="", blank="", verbose_name="优惠类型")

    class Meta:
        db_table = "ly_order_detail"
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.course.name)