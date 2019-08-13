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