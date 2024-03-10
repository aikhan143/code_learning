from django.db import models
from django.contrib.auth import get_user_model

from projects.models import *

User = get_user_model()

class Payment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='Payment Intent ID')
    is_paid = models.BooleanField(default=False)