# Generated by Django 5.1.1 on 2024-10-18 10:19

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=221, null=True, verbose_name='Nomi')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': "Bo'limlar",
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='PDFInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=221, null=True, verbose_name='Fayl nomi')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='pdfs/', verbose_name='PDF file')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Yaratilgan vaqti')),
            ],
            options={
                'verbose_name': 'pdf_information',
                'verbose_name_plural': 'PDF File',
                'db_table': 'pdf_file',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='F.I.Sh')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Username')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Telefon raqam')),
                ('telegram_id', models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='Telegram ID')),
                ('role', models.CharField(blank=True, choices=[('hr', 'HR xodim'), ('user', 'Oddiy foydalanuvchi'), ('teacher', "Ish o'rgatuvchi maxsus xodim"), ('intern', 'Stajor'), ('chief', "Bo'lim boshlig'i"), ('admin', 'Admin')], default='user', max_length=100, null=True, verbose_name='Foydalanuvchi roli')),
                ('joined_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 18, 15, 19, 25, 555480), null=True, verbose_name="Qo'shilgan vaqti")),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Foydalanuvchilar',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 18, 15, 19, 25, 555480), null=True, verbose_name='Yaratilgan vaqti')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intern.department', verbose_name="Bo'lim")),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intern.users', verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Ustoz xodimlar',
                'db_table': 'teacher_profile',
            },
        ),
        migrations.CreateModel(
            name='InternProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internship_period', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(90)], verbose_name='Stajirovka muddati')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Aktivligi')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 18, 15, 19, 25, 556479), null=True, verbose_name='Yaratilgan vaqti')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intern.department', verbose_name="Bo'lim")),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='intern.teacherprofile', verbose_name="Ish o'rgatuchi")),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intern.users', verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Intern',
                'verbose_name_plural': 'Stajorlar',
                'db_table': 'intern_profile',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('muomala', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Muomala madaniyati')),
                ('kirishimlilik', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Kirishimliligi')),
                ('chaqqonlik_va_malaka', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Chaqqonligi va malakasi')),
                ('masuliyat', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name="Mas'uliyati")),
                ('ozlashtirish_qobiliyati', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name="O'zlashtirish qobiliyati")),
                ('ichki_tartibga_rioyasi', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Ichki tartibga rioya qilishi')),
                ('shaxsiy_intizomi', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Shaxsiy intizomi')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Izoh')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 18, 15, 19, 25, 557544), null=True, verbose_name='Baholangan vaqt')),
                ('intern', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intern.internprofile', verbose_name='Stajor')),
                ('rated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='intern.users', verbose_name='Baholagan shaxs')),
            ],
            options={
                'verbose_name': 'Mark',
                'verbose_name_plural': 'Baholar',
                'db_table': 'mark',
            },
        ),
        migrations.CreateModel(
            name='HrProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 18, 15, 19, 25, 557478), null=True, verbose_name='Yaratilgan vaqti')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intern.users', verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Hr',
                'verbose_name_plural': 'Hr xodimlar',
                'db_table': 'hr_profile',
            },
        ),
        migrations.CreateModel(
            name='ChiefProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 18, 15, 19, 25, 556479), null=True, verbose_name='Yaratilgan vaqti')),
                ('department', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intern.department', verbose_name="Bo'lim")),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intern.users', verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Chief',
                'verbose_name_plural': "Bo'lim boshliqlari",
                'db_table': 'chief_profile',
            },
        ),
    ]
