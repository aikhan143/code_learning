from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length= 255, blank=False, null=False)
    file = models.FileField(upload_to= 'videos/',null=True)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE, )

    def __repr__(self):
        return 'Resume(%s, %s)' % (self.title, self.file)

    def __str__ (self):
        return self.title
