from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
PRIORITY_CHOICES = (
    ('L', 'Low'),
    ('M', 'Medium'),
    ('U', 'Urgent'),
    )

class Teams(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

class Workflows(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    dueDate = models.DateField()
    priority = models.CharField(max_length=1, choices = PRIORITY_CHOICES)

    #Unique workflows per user test
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True)
class User(AbstractUser):

        MANAGER = 1
        CLIENT = 2

        ROLE_CHOICES = (
            (MANAGER, 'Manager'),
            (CLIENT,'Client')
        )
        role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
        user = User.objects.first()
        user.role = User.CLIENT
        user.save()
        user.role == USER.MANAGER
        False
        user.role == USER.CLIENT
        True