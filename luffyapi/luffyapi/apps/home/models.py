from django.db import models
from luffyapi.utils.models import BaseModel
# Create your models here.
class BannerInfo(BaseModel):
    """
    轮播图
    """
    # upload_to 存储子目录，真实存放地址会使用配置中的MADIE_ROOT+upload_to
    image = models.ImageField(upload_to='banner', verbose_name='轮播图', null=True,blank=True)
    name = models.CharField(max_length=150, verbose_name='轮播图名称')
    note = models.CharField(max_length=150, verbose_name='备注信息')
    link = models.CharField(max_length=150, verbose_name='轮播图广告地址')

    class Meta:
        db_table = 'ly_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class NavInfo(BaseModel):
    """导航"""
    # 导航位置
    NAV_OPTION = (
        (1,"头部导航"),
        (2,"脚部导航"),
    )
    name = models.CharField(max_length=150, verbose_name='导航名称')
    link = models.CharField(max_length=150, verbose_name='导航链接地址')
    opt = models.SmallIntegerField(choices=NAV_OPTION,default=1, verbose_name="导航位置")

    class Meta:
        db_table = 'ly_nav'
        verbose_name = '导航'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
