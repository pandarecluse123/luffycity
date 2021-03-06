# 主程序
import os
from celery import Celery
# 创建celery实例对象
app = Celery("luffy")


#把celery 和django进行组合,识别和加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE','luffyapi.settings.dev')

#在当前celery中启动django框架,进行初始化

import django
django.setup()
# 通过app对象加载配置
app.config_from_object("celery_tasks.config")

# 自动搜索并加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["celery_tasks.sms",'celery_tasks.order'])

# 启动Celery的命令
# 强烈建议切换目录到项目的根目录下启动celery!!
#celery -A celery_tasks.maib22efab2-0e31-4643-99c8-7859be99d282\", \"date_done\": \"2019-n worker --loglevel=info