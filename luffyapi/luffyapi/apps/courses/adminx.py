import xadmin

from .models import CourseCategory
class CourseCategoryModelAdmin(object):
    pass
xadmin.site.register(CourseCategory,CourseCategoryModelAdmin)

from .models import Course
class CourseModelAdmin(object):
    pass
xadmin.site.register(Course,CourseModelAdmin)

from .models import Teacher
class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass
xadmin.site.register(Teacher, TeacherModelAdmin)


from .models import CourseChapter
class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    pass
xadmin.site.register(CourseChapter, CourseChapterModelAdmin)



from .models import CourseLesson
class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    pass
xadmin.site.register(CourseLesson, CourseLessonModelAdmin)

from .models import CourseExpire
class CourseExpireModelAdmin(object):
    """课程课时模型管理类"""
    pass
xadmin.site.register(CourseExpire, CourseExpireModelAdmin)


from .models import PriceDiscount
class PriceDiscountModelAdmin(object):
    pass
xadmin.site.register(PriceDiscount, PriceDiscountModelAdmin)


from .models import CoursePriceDiscount
class CoursePriceDiscountModelAdmin(object):
    pass
xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)



from .models import PriceDiscountType
class PriceDiscountTypeModelAdmin(object):
    pass
xadmin.site.register(PriceDiscountType, PriceDiscountTypeModelAdmin)

from .models import Activity
class ActivityModelAdmin(object):
    pass
xadmin.site.register(Activity, ActivityModelAdmin)
