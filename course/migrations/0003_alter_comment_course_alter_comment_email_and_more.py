# Generated by Django 4.1.3 on 2022-11-22 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0002_alter_comment_options_alter_course_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='course.course', verbose_name='دوره'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='full_name',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='نام کامل'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='course.comment', verbose_name='کامنت والد'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='متن نظر'),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[('mobile_developer', 'برنامه نویسی موبایل'), ('web_developer', 'برنامه نویسی وب'), ('graphics', 'گرافیک'), ('AI', 'هوش مصنوعی')], max_length=20, verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='course',
            name='free',
            field=models.BooleanField(default=False, verbose_name='رایگان'),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, help_text='دست نزنید', verbose_name='اسلاگ'),
        ),
        migrations.AlterField(
            model_name='headline',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='headlines', to='course.course', verbose_name='دوره'),
        ),
        migrations.AlterField(
            model_name='headline',
            name='title',
            field=models.CharField(max_length=250, verbose_name='عنوان سر فصل'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribes', to='course.course', verbose_name='دوره'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribes', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='video',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='course.course', verbose_name='دوره'),
        ),
        migrations.AlterField(
            model_name='video',
            name='headline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='course.headline', verbose_name='سرفصل'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=150, verbose_name='عنوان ویدئو'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='course/video', verbose_name='فایل ویدئو'),
        ),
    ]