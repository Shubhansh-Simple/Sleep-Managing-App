# Generated by Django 2.2 on 2020-12-18 13:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sleep_manage_app', '0007_auto_20201218_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sleep',
            name='your_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Day'),
        ),
    ]
