# Generated by Django 5.1.1 on 2024-10-11 06:32

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0008_remove_mark_chief_remove_mark_hr_remove_mark_teacher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chiefprofile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 11, 11, 32, 27, 35849), null=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='hrprofile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 11, 11, 32, 27, 36848), null=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='internprofile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 11, 11, 32, 27, 35849), null=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 11, 11, 32, 27, 36848), null=True, verbose_name='Baholangan vaqt'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='rated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='intern.users', verbose_name='Baholagan shaxs'),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 11, 11, 32, 27, 35849), null=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='users',
            name='joined_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 11, 11, 32, 27, 34848), null=True, verbose_name="Qo'shilgan vaqti"),
        ),
    ]
