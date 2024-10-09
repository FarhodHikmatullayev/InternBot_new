from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class Users(models.Model):
    ROLE_CHOICES = (
        ('hr', 'HR xodim'),
        ('user', 'Oddiy foydalanuvchi'),
        ('teacher', "Ish o'rgatuvchi maxsus xodim"),
        ('intern', 'Stajor'),
        ('chief', "Bo'lim boshlig'i"),
        ('admin', 'Admin')
    )
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='F.I.Sh')
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name='Username')
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name='Telefon raqam')
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name="Telegram ID")
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user', null=True, blank=True,
                            verbose_name='Foydalanuvchi roli')
    joined_at = models.DateTimeField(null=True, blank=True, default=datetime.now(), verbose_name="Qo'shilgan vaqti")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'
        db_table = 'users'

    def __str__(self):
        return self.full_name


class Department(models.Model):
    name = models.CharField(max_length=221, null=True, blank=True, verbose_name="Nomi")

    class Meta:
        db_table = "department"
        verbose_name = "Department"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Foydalanuvchi')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Bo'lim")
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.now(), verbose_name="Yaratilgan vaqti")

    class Meta:
        db_table = "teacher_profile"
        verbose_name = "Teacher"
        verbose_name_plural = "Ustoz xodimlar"

    def __str__(self):
        return self.user.full_name


class ChiefProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Foydalanuvchi')
    department = models.OneToOneField(Department, on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name="Bo'lim")
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.now(), verbose_name="Yaratilgan vaqti")

    class Meta:
        db_table = "chief_profile"
        verbose_name = "Chief"
        verbose_name_plural = "Bo'lim boshliqlari"

    def __str__(self):
        return self.user.full_name


class InternProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Foydalanuvchi")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="Ish o'rgatuchi")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Bo'lim")
    internship_period = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(90)
    ], verbose_name="Stajirovka muddati")
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.now(), verbose_name="Yaratilgan vaqti")

    class Meta:
        db_table = 'intern_profile'
        verbose_name = 'Intern'
        verbose_name_plural = "Stajorlar"

    def __str__(self):
        return self.user.full_name


class HrProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Foydalanuvchi")
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.now(), verbose_name="Yaratilgan vaqti")

    class Meta:
        db_table = 'hr_profile'
        verbose_name = 'Hr'
        verbose_name_plural = "Hr xodimlar"

    def __str__(self):
        return self.user.full_name


class Mark(models.Model):
    intern = models.ForeignKey(InternProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Stajor")
    muomala = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='Muomala madaniyati'
    )
    kirishimlilik = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='Kirishimliligi'
    )
    chaqqonlik_va_malaka = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='Chaqqonligi va malakasi'
    )
    masuliyat = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name="Mas'uliyati"
    )
    ozlashtirish_qobiliyati = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name="O'zlashtirish qobiliyati"
    )
    ichki_tartibga_rioyasi = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name="Ichki tartibga rioya qilishi"
    )
    shaxsiy_intizomi = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='Shaxsiy intizomi'
    )
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="Ish o'rgatuvchi")
    description = models.TextField(null=True, blank=True, verbose_name='Izoh')
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.now(), verbose_name='Yaratilgan vaqt')

    class Meta:
        db_table = 'mark'
        verbose_name = 'Mark'
        verbose_name_plural = 'Baholar'

    def __str__(self):
        return self.intern
