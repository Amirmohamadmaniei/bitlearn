# Generated by Django 4.1.3 on 2022-11-21 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': 'مقاله', 'verbose_name_plural': 'مقالات'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته بندی مقالات', 'verbose_name_plural': 'دسته بندی های مقالات'},
        ),
        migrations.AlterModelOptions(
            name='commentblog',
            options={'verbose_name': 'نظر', 'verbose_name_plural': 'نظرات'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'برچسب مقالات', 'verbose_name_plural': 'برچسب های مقالات'},
        ),
    ]
