# Generated by Django 2.2.4 on 2019-08-19 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20190815_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseExpire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.IntegerField(verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('expire_time', models.IntegerField(blank=True, null=True, verbose_name='有效期数值')),
                ('expire_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='有效期文本')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='课程价格')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_expire', to='courses.Course', verbose_name='课程名')),
            ],
            options={
                'verbose_name': '课程有效期选项',
                'verbose_name_plural': '课程有效期选项',
                'db_table': 'ly_course_expire',
            },
        ),
    ]