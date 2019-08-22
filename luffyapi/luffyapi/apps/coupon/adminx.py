import xadmin
from .models import Coupon,UserCoupon
class CouponModelAdmin(object):
    pass

xadmin.site.register(Coupon,CouponModelAdmin)

class UserCouponModelAdmin(object):
    pass
xadmin.site.register(UserCoupon,UserCouponModelAdmin)