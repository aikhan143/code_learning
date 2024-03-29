# Generated by Django 5.0.2 on 2024-03-11 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image_dark',
            field=models.ImageField(blank=True, upload_to='img_for_course', verbose_name='Картинка для курсов(тёмная)'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image_light',
            field=models.ImageField(blank=True, upload_to='img_for_course', verbose_name='Картинка для курсов(светлая)'),
        ),
    ]
