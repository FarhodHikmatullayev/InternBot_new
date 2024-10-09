# Generated by Django 5.1.1 on 2024-10-09 09:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0005_alter_chiefprofile_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chiefprofile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 9, 14, 16, 39, 193072), null=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='hrprofile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 9, 14, 16, 39, 193072), null=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='internprofile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 9, 14, 16, 39, 193072), null=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 9, 14, 16, 39, 194069), null=True, verbose_name='Yaratilgan vaqt'),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 9, 14, 16, 39, 192070), null=True, verbose_name='Yaratilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='users',
            name='joined_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 9, 14, 16, 39, 192070), null=True, verbose_name="Qo'shilgan vaqti"),
        ),
    ]
