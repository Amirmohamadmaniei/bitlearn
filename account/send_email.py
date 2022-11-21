from random import randint
from django.core.mail import send_mail
from BitLearn import settings
from account.models import OTP


def send_email(user, email):
    rand_num = randint(1000, 9999)
    OTP.objects.create(email=email, code=rand_num)
    subject = 'تایید ایمیل برای ثبت نام در بیت لرن'
    message = f'با سلام ، تشکر برای ثبت نام در سایت ما \n {rand_num} : کد تایید شما'
    email_form = settings.EMAIL_HOST_USER
    ricipient_user = [user, email, ]
    send_mail(subject, message, email_form, ricipient_user)
