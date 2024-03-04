from django.db import models
from slugify import slugify

class Course(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50, blank=True)
    title = models.CharField(max_length=50, unique=True, verbose_name='Course name')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Course price')
    is_paid = models.BooleanField(default=False)

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
    user_answer = models.TextField(verbose_name='User code')
    statuses = [
        ('D', 'Done'),
        ('ND', 'Not Done')
    ]
    status = models.CharField(max_length=2, choices=statuses, default='ND', blank=True)

    def __str__(self):
        return self.title
    
    def is_user_answer_correct(self):
        if self.user_answer == self.correct_answer:
            self.status= 'D'
            self.save()
