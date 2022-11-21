# Generated by Django 4.1.3 on 2022-11-21 13:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='عنوان دوره نباید تکراری باشد', max_length=200, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('level', models.CharField(choices=[('preliminary', 'مقدماتی'), ('medium', 'متوسط'), ('advanced', 'پیشرفته')], max_length=20, verbose_name='سطح')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('discount', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='تخفیف')),
                ('price_with_discount', models.IntegerField(default=0)),
                ('introduction_video', models.FileField(upload_to='course/video/introduction', verbose_name='ویدئوی معرفی')),
                ('image', models.ImageField(help_text='سایز عکس 600 در 300 باشد', upload_to='course/image/introduction', verbose_name='عکس')),
                ('status', models.CharField(choices=[('soon', 'به زودی'), ('on-performing', 'در حال برگزاری'), ('finished', 'به اتمام رسیده')], default=0, max_length=20, verbose_name='وضعیت دوره')),
                ('free', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('mobile_developer', 'برنامه نویسی موبایل'), ('web_developer', 'برنامه نویسی وب'), ('graphics', 'گرافیک'), ('AI', 'هوش مصنوعی')], max_length=20)),
                ('publish', models.BooleanField(default=False, verbose_name='انتشار')),
                ('slug', models.SlugField(allow_unicode=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='account.profile', verbose_name='مدرس')),
            ],
        ),
        migrations.CreateModel(
            name='Headline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='headlines', to='course.course')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('video', models.FileField(upload_to='course/video')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='course.course')),
                ('headline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='course.headline')),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribes', to='course.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='course.course')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='course.comment')),
            ],
        ),
    ]
