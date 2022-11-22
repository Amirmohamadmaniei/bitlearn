from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account.models import CustomUser, Profile
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from course.choices import level_choices, status_choices, category_choices


class Course(models.Model):
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses', verbose_name='مدرس')
    title = models.CharField(max_length=200, help_text='عنوان دوره نباید تکراری باشد', verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')

    level = models.CharField(max_length=20, choices=level_choices, verbose_name='سطح')
    price = models.IntegerField(verbose_name='قیمت')
    discount = models.IntegerField(verbose_name='تخفیف', validators=[MaxValueValidator(100), MinValueValidator(0)])
    price_with_discount = models.IntegerField(default=0)
    introduction_video = models.FileField(upload_to='course/video/introduction', verbose_name='ویدئوی معرفی')
    image = models.ImageField(upload_to='course/image/introduction', verbose_name='عکس',
                              help_text='سایز عکس 600 در 300 باشد')

    status = models.CharField(max_length=20, choices=status_choices, default=0, verbose_name='وضعیت دوره')
    free = models.BooleanField(default=False, verbose_name='رایگان')
    category = models.CharField(max_length=20, choices=category_choices, verbose_name='دسته بندی')
    publish = models.BooleanField(default=False, verbose_name='انتشار')

    slug = models.SlugField(blank=True, allow_unicode=True, verbose_name='اسلاگ', help_text='دست نزنید')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        return reverse('course:detail', kwargs={'slug': self.slug})

    @property
    def status_fa(self):
        if self.status == 'soon':
            return 'به زودی'
        if self.status == 'on-performing':
            return 'در حال برگزاری'
        if self.status == 'finished':
            return 'به اتمام رسیده'
        else:
            return ''

    @property
    def level_fa(self):
        if self.level == 'preliminary':
            return 'مقدماتی'
        if self.level == 'medium':
            return 'متوسط'
        if self.level == 'advanced':
            return 'پیشرفته'
        else:
            return ''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        if self.free is False:
            if self.discount != 0:
                self.price_with_discount = self.price - (self.price * self.discount // 100)
            else:
                self.price_with_discount = self.price
        else:
            self.price = 0
            self.price_with_discount = 0
            self.discount = 0
        return super(Course, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'


class Headline(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان سر فصل')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='headlines', verbose_name='دوره')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'سرفصل'
        verbose_name_plural = 'سرفصل ها'


class Video(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان ویدئو')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos', verbose_name='دوره')
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE, related_name='videos', verbose_name='سرفصل')
    video = models.FileField(upload_to='course/video', verbose_name='فایل ویدئو')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ویدئو'
        verbose_name_plural = 'ویدئو ها'


class Subscribe(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscribes', verbose_name='دوره')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscribes', verbose_name='کاربر')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} {self.course}'

    class Meta:
        verbose_name = 'اشتراک'
        verbose_name_plural = 'اشتراک ها'


class Comment(models.Model):
    full_name = models.CharField(max_length=120, null=True, blank=True, verbose_name='نام کامل')
    email = models.EmailField(verbose_name='ایمیل')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name='دوره')
    text = models.TextField(verbose_name='متن نظر')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                               verbose_name='کامنت والد')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}-{self.course}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
