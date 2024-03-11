from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()

class Course(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50, blank=True)
    title = models.CharField(max_length=50, unique=True, verbose_name='Course name')
    image_light = models.ImageField(upload_to='img_for_course', verbose_name='Картинка для курсов(светлая)', blank=True) 
    image_dark = models.ImageField(upload_to='img_for_course', verbose_name='Картинка для курсов(тёмная)', blank=True)  
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class Project(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50, blank=True)
    title = models.CharField(max_length=50, unique=True, verbose_name='Project name')
    description = models.TextField(verbose_name='Project description')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='projects')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Project price')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=10, unique=True, verbose_name='Task name')
    description = models.TextField(verbose_name='Task description')
    correct_answer = models.TextField(verbose_name='Correct code', blank=True)
    slug = models.SlugField(primary_key=True, max_length=50, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class TaskUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_user')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_user')
    user_answer = models.TextField(verbose_name='User code')
    statuses = [
        ('D', 'Done'),
        ('ND', 'Not Done')
    ]
    status = models.CharField(max_length=2, choices=statuses, default='ND', blank=True)
