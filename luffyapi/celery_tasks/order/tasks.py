from celery_tasks.main import app
from datetime import datetime
from django.conf import settings
from order.models import Order

#先执行celery -A celery_tasks.main beat,再执行worker的主程序
@app.task(name='check_order')
def check_order():
    now=datetime.now().timestamp()
    out_time=now-settings.ORDER_TIMER
    out_time=datetime.fromtimestamp(out_time)
    time_out_list=Order.objects.filter(order_status=0,created_time__lt=out_time)
    for order in time_out_list:
        order.order_status=3
        order.save()