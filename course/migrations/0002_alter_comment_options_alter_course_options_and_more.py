# Generated by Django 4.1.3 on 2022-11-21 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'نظر', 'verbose_name_plural': 'نظرات'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'دوره', 'verbose_name_plural': 'دوره ها'},
        ),
        migrations.AlterModelOptions(
            name='headline',
            options={'verbose_name': 'سرفصل', 'verbose_name_plural': 'سرفصل ها'},
        ),
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'اشتراک', 'verbose_name_plural': 'اشتراک ه'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'ویدئو', 'verbose_name_plural': 'ویدئو ها'},
        ),
    ]
