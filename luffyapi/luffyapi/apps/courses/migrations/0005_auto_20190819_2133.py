# Generated by Django 2.2.4 on 2019-08-19 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_courseexpire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='此价格为永久购买的价格', max_digits=6, verbose_name='课程原价'),
        ),
    ]
