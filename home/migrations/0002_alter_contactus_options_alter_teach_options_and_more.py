# Generated by Django 4.1.3 on 2022-11-21 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'verbose_name': 'ارتباط با ما', 'verbose_name_plural': 'ارتباط با ما'},
        ),
        migrations.AlterModelOptions(
            name='teach',
            options={'verbose_name': 'درخواست مدرسی', 'verbose_name_plural': 'درخواست های مدرسی'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'تیکت', 'verbose_name_plural': 'تیکت ها'},
        ),
    ]
