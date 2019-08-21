from django.db import models
from luffyapi.utils.models import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
# Create your models here.


class CourseCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")
    class Meta:
        db_table = "ly_course_category"
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"


    def __str__(self):
        return "%s" % self.name



class Course(BaseModel):
    """
    专题课程
    """
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="course", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type,default=0, verbose_name="付费类型")
    course_video = models.FileField(upload_to="course", max_length=255, verbose_name="封面视频", blank=True, null=True)
    # 使用这个字段的原因
    # brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    brief = RichTextUploadingField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.FileField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True,verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数",default = 0)
    lessons = models.IntegerField(verbose_name="总课时数量",default = 0)
    pub_lessons = models.IntegerField(verbose_name="课时更新数量",default = 0)
    price = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="课程原价",default=0,help_text='此价格为永久购买的价格')
    teacher = models.ForeignKey("Teacher",on_delete=models.DO_NOTHING, null=True, blank=True,verbose_name="授课老师")
    class Meta:
        db_table = "ly_course"
        verbose_name = "专题课程"
        verbose_name_plural = "专题课程"

    @property
    def lesson_list(self):
        lesson_list=self.courselessons.filter(is_show_list=True,).order_by('chapter_id')[:4]
        data=[]

        if len(lesson_list)<1:
            return data

        for lesson in lesson_list:
            data.append({
                'name':lesson.name,
                'id':lesson.id,
                'chapter':lesson.chapter.chapter,
                'free_trail':True if lesson.free_trail==True else False
            })
        return data

    @property
    def level_name(self):
        return self.level_choices[self.level][1]

    @property
    def real_brief(self):
        return self.brief.replace("/media",settings.CKEDITOR_UPLOAD_URL+"/media")

    @property
    def chapter_list(self):
        chapter_list=self.coursechapters.filter(is_delete=False,is_show=True).order_by('chapter')
        data=[]
        for chapter in chapter_list:
            chapter_lesson=chapter.coursesections.filter(is_delete=False,is_show=True)
            lesson_list=[]
            for lesson in chapter_lesson:
                lesson_list.append({
                    'id':lesson.id,
                    'name':lesson.name,
                    'section_type':lesson.section_type,
                    'free_trail':lesson.free_trail
                })
            data.append({
                'chapter':chapter.chapter,
                'name':chapter.name,
                'lesson_list':lesson_list,
            })
        return data

    @property
    def expire_list(self):
        data=[]
        expire_list=self.course_expire.all().order_by('-expire_time')
        for item in expire_list:
            data.append({
                'expire_text':item.expire_text,
                'price':self.real_price(item.price),
                'expire_time':item.expire_time

            })

        if self.price>0:
            data.append({
                'expire_text': '永久有效',
                'price': self.real_price(),
                'expire_time': 0
            })

        return data

    @property
    def discount_name(self):
        discount_list=self.course_discount.filter(is_show=True,is_delete=False).first()
        if discount_list is None:
        #没有查到所有的优惠信息
            return None
        discount_name=discount_list.discount.discount_type

        return discount_name.name


    def real_price(self,price=None):
        if  price is None:
            price=self.price
        price=float(price)
        discount_list=self.course_discount.filter(is_show=True,is_delete=False).first()

        if not discount_list:
            return price

        activity=discount_list.active

        start_time=activity.start_time.timestamp()
        end_time=activity.end_time.timestamp()

        from datetime import datetime

        current_time=datetime.now().timestamp()

        if current_time<=start_time or current_time>=end_time:
            return price


        discount=discount_list.discount

        if discount.sale=='':
            return 0
        elif discount.sale[0]=='*':
            sale=float(discount.sale[1:])
            print(sale,type(sale))
            print(price,type(price))
            # return '%.2f'%(price*float(discount.sale[1:]))
            return (price * sale)

        elif discount.sale[0]=='-':
            return '%.2f'%(price-float(discount.sale[1:]))

        elif discount.sale[0]=='满':
            data=[]
            sale_msg_list=discount.sale.split('\r\n')
            for sale_msg in sale_msg_list:
                if price>float(sale_msg[1:].split('-')[0]):
                    data.append(float(sale_msg[1:].split('-')[1]))
            return '%.2f'%(price-max(data))

    def active_time(self):
        from datetime import datetime
        now = datetime.now()
        try:
            active=self.course_discount.get(active__created_time__lt=now,active__end_time__gt=now)
        except:
            return 0
        now = datetime.now().timestamp()
        active_time=active.active.end_time.timestamp()-now
        return active_time


    def __str__(self):
        return "%s" % self.name



class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师title")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name = "讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "ly_teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "ly_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseLesson(BaseModel):
    """课程课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,verbose_name="课程章节")
    name = models.CharField(max_length=128,verbose_name = "课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接", help_text = "若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)
    is_show_list=models.BooleanField(verbose_name='是否展示到列表页',default=False)
    course=models.ForeignKey('Course',related_name='courselessons',on_delete=models.CASCADE,verbose_name='课程名称')
    chapter_nb=models
    class Meta:
        db_table = "ly_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


class CourseExpire(BaseModel):
    course=models.ForeignKey('Course',related_name='course_expire',verbose_name='课程名',on_delete=models.CASCADE)
    expire_time=models.IntegerField(verbose_name='有效期数值',null=True,blank=True)
    expire_text=models.CharField(max_length=255,verbose_name='有效期文本',null=True,blank=True)
    price=models.DecimalField(verbose_name='课程价格',default=0,max_digits=6,decimal_places=2)

    class Meta():
        db_table='ly_course_expire'
        verbose_name='课程有效期选项'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '课程:%s 有效期:%s 课程价格:%s'%(self.course,self.expire_time,self.price)


# 价格相关的模型

class PriceDiscountType(BaseModel):
    name=models.CharField(max_length=32,verbose_name='优惠类型')
    remarke=models.CharField(max_length=150,verbose_name='备注信息',null=True,blank=True)

    class Meta:
        db_table='ly_discount_type'
        verbose_name='优惠类型'
        verbose_name_plural=verbose_name

    def __str__(self):
        return ' %s'%self.name

class PriceDiscount(BaseModel):
    discount_type=models.ForeignKey('PriceDiscountType',on_delete=models.CASCADE,related_name='pricediscount',verbose_name='优惠类型')
    condition=models.IntegerField(blank=True,default=0,verbose_name='满足优惠的条件',help_text="设置参与优惠的价格门槛，表示商品必须在xx价格以上的时候才参与优惠活动，<br>如果不填，则不设置门槛")
    sale=models.TextField(verbose_name='优惠公式',blank=True,null=True,help_text="""
     不填表示免费；<br>
    *号开头表示折扣价，例如*0.82表示八二折；<br>
    -号开头则表示减免，例如-20表示原价-20；<br>
    如果需要表示满减,则需要使用 原价-优惠价格,例如表示课程价格大于100,优惠10;大于200,优惠20,格式如下:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-20<br>
    """)

    class Meta:
        db_table='ly_price_discount'
        verbose_name='价格优惠计算'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '价格优惠:%s,优惠条件:%s,优惠公式:%s'%(self.discount_type,self.condition,self.sale)

class CoursePriceDiscount(BaseModel):
    course=models.ForeignKey('Course',verbose_name='课程',on_delete=models.CASCADE,related_name='course_discount')
    active=models.ForeignKey('Activity',verbose_name='活动',on_delete=models.DO_NOTHING,related_name='activity_discount')
    discount=models.ForeignKey('PriceDiscount',verbose_name='优惠信息',on_delete=models.CASCADE,related_name='discount_discount')

    class Meta:
        db_table='ly_course_price_discount'
        verbose_name='课程优惠关系表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "课程：%s，优惠活动: %s,开始时间:%s,结束时间:%s" % (self.course.name, self.active.name, self.active.start_time,self.active.end_time)

class Activity(BaseModel):
    name=models.CharField(max_length=150,verbose_name='活动名称')
    start_time=models.DateTimeField(verbose_name='活动的开始时间')
    end_time=models.DateTimeField(verbose_name='活动的结束时间')
    remark=models.CharField(max_length=150,verbose_name='备注',blank=True,null=True)

    class Meta:
        db_table='ly_active'
        verbose_name='活动信息'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name