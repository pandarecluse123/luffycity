from rest_framework import serializers
from .models import CourseCategory,Course,Teacher

class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta():
        model=CourseCategory
        fields=['id','name']

class CourseTeacherModelSerializer(serializers.ModelSerializer):
    class Meta():
        model=Teacher
        fields=['name','title','signature']

class CourseModelSerializer(serializers.ModelSerializer):
    teacher=CourseTeacherModelSerializer() #一对一
    # teacher=CourseTeacherModelSerializer(many=True) #一对多

    class Meta():
        model=Course
        fields=['id','name','course_img','students','price','teacher','lessons','pub_lessons','lesson_list']


class CourseDetailTeacherModelSerializer(serializers.ModelSerializer):
    class Meta():
        model=Teacher
        fields=['name','image','brief','role']


class CourseDetailModelSerializer(serializers.ModelSerializer):
    teacher=CourseDetailTeacherModelSerializer()
    class Meta():
        model=Course
        fields=['name','course_video','real_brief','course_img','students','price','teacher','lessons','pub_lessons','chapter_list','level_name']