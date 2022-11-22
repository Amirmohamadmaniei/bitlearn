from django.db import models
from account.models import CustomUser
from course.choices import category_choices


class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets', verbose_name='کاربر')
    subject = models.CharField(max_length=50, verbose_name='موضوع')
    body = models.TextField(verbose_name='پیام')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


class Teach(models.Model):
    full_name = models.CharField(max_length=120, verbose_name='نام کامل')
    tel = models.CharField(max_length=11, verbose_name='تلفن')
    email = models.EmailField(verbose_name='ایمیل')
    title = models.CharField(max_length=80, verbose_name='عنوان')
    category = models.CharField(max_length=20, choices=category_choices, verbose_name='دسته بندی')
    link = models.URLField(max_length=120, verbose_name='لینک ویدئو')
    description = models.TextField(verbose_name='توضیحات')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'درخواست مدرسی'
        verbose_name_plural = 'درخواست های مدرسی'


class ContactUs(models.Model):
    full_name = models.CharField(max_length=120, verbose_name='نام کامل')
    email = models.EmailField(verbose_name='ایمیل')
    body = models.TextField(verbose_name='پیام')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'ارتباط با ما'
        verbose_name_plural = 'ارتباط با ما'
