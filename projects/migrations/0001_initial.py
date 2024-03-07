# Generated by Django 5.0.2 on 2024-03-06 13:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('slug', models.SlugField(blank=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Course name')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('slug', models.SlugField(blank=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Project name')),
                ('description', models.TextField(verbose_name='Project description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Project price')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='projects.course')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('title', models.CharField(max_length=10, unique=True, verbose_name='Task name')),
                ('description', models.TextField(verbose_name='Task description')),
                ('correct_answer', models.TextField(blank=True, verbose_name='Correct code')),
                ('slug', models.SlugField(blank=True, primary_key=True, serialize=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='TaskUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.TextField(verbose_name='User code')),
                ('status', models.CharField(blank=True, choices=[('D', 'Done'), ('ND', 'Not Done')], default='ND', max_length=2)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_user', to='projects.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
