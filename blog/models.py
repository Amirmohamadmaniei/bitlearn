from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account.models import CustomUser
from course.models import Comment


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس ip')

    class Meta:
        verbose_name = 'آدرس IP'
        verbose_name_plural = 'آدرس های IP'


class Category(models.Model):
    title = models.CharField(max_length=80, verbose_name='عنوان دسته بندی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'


class Tag(models.Model):
    title = models.CharField(max_length=40, verbose_name='عنوان برچسب')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برچسب مقالات'
        verbose_name_plural = 'برچسب های مقالات'


class Blog(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs', verbose_name='نویسنده')
    title = models.CharField(max_length=90, verbose_name='عنوان')
    body = models.TextField(verbose_name='متن اصلی')
    image = models.ImageField(upload_to='blog/img', verbose_name='عکس')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', verbose_name='دسته بندی')
    tag = models.ManyToManyField(Tag, verbose_name='برچسب ها')
    view = models.ManyToManyField(IPAddress, verbose_name='بازدید ها')

    slug = models.SlugField(null=True, blank=True, allow_unicode=True, verbose_name='اسلاگ', help_text='دست نزنید')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class CommentBlog(models.Model):
    full_name = models.CharField(max_length=60, null=True, blank=True, verbose_name='نام کامل')
    email = models.EmailField(verbose_name='ایمیل')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    text = models.TextField(verbose_name='متن نظر')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                               verbose_name='کامنت والد')

    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.full_name}-{self.blog}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
