from django.db import models
from django.contrib.auth.models import User
# Create your models here.
PRIORITY_CHOICES = (
    ('L', 'Low'),
    ('M', 'Medium'),
    ('U', 'Urgent'),
    )
class Workflows(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    dueDate = models.DateField()
    priority = models.CharField(max_length=1, choices = PRIORITY_CHOICES)

    #Unique workflows per user test
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
