# Generated by Django 4.1.3 on 2022-11-23 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blog_author_alter_blog_body_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentblog',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='view',
            field=models.ManyToManyField(to='blog.ipaddress', verbose_name='بازدید ها'),
        ),
    ]
