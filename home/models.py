from django.db import models
from account.models import CustomUser
from course.choices import category_choices


class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=50)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


class Teach(models.Model):
    full_name = models.CharField(max_length=120)
    tel = models.CharField(max_length=11)
    email = models.EmailField()
    title = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=category_choices)
    link = models.URLField(max_length=120)
    description = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'درخواست مدرسی'
        verbose_name_plural = 'درخواست های مدرسی'


class ContactUs(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'ارتباط با ما'
        verbose_name_plural = 'ارتباط با ما'
