from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from account.models import CustomUser
from course.models import Comment


class Category(models.Model):
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'


class Tag(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برچسب مقالات'
        verbose_name_plural = 'برچسب های مقالات'


class Blog(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=90)
    body = models.TextField()
    image = models.ImageField(upload_to='blog/img')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')
    tag = models.ManyToManyField(Tag)
    view = models.IntegerField(default=0)

    slug = models.SlugField(null=True, blank=True, allow_unicode=True)

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
    full_name = models.CharField(max_length=60, null=True, blank=True)
    email = models.EmailField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f'{self.full_name}-{self.blog}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
