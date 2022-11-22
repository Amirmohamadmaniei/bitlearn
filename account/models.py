from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserAdmin(BaseUserManager):
    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError('کاربر باید دارای ایمیل باشد')

        user = self.model(email=self.normalize_email(email), phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None):
        user = self.create_user(email, password=password, phone=phone)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    fname = models.CharField(max_length=150, null=True, blank=True, verbose_name='نام')
    lname = models.CharField(max_length=150, null=True, blank=True, verbose_name='نام خانوادگی')
    email = models.EmailField(unique=True, verbose_name='ایمیل(نام کاربری)')
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')

    is_active = models.BooleanField(default=False, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_teacher = models.BooleanField(default=False, verbose_name='مدرس')

    object = CustomUserAdmin()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def save(self, *args, **kwargs):
        if self.is_teacher is True:
            try:
                Profile.objects.create(user_id=self.id)
            except:
                pass
        return super(CustomUser, self).save(*args, **kwargs)

    @property
    def get_full_name(self):
        if self.fname is None:
            return self.lname
        if self.lname is None:
            return self.fname
        return f'{self.fname} {self.lname}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب های کاربری'


class OTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=10)
    expiration = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'کد اعتبار سنجی'
        verbose_name_plural = 'کد های اعتبار سنجی'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', verbose_name='مدرس')
    description = models.TextField(verbose_name='بیوگرافی')
    image = models.ImageField(upload_to='photo/teacher', null=True, blank=True, verbose_name='عکس پروفایل')
    grade = models.CharField(max_length=30, verbose_name='مدرک تحصیلی')
    major = models.CharField(max_length=30, verbose_name='رشته تحصیلی')
    university = models.CharField(max_length=80, verbose_name='دانشگاه')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'پروفایل مدرس'
        verbose_name_plural = 'پروفایل مدرس ها'


class Skill(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills', verbose_name='مدرس')
    title = models.CharField(max_length=50, verbose_name='عنوان')
    percentage = models.IntegerField(verbose_name='میزان درصد')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت ها'
