from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='custom_user_set',  # Custom related_name to avoid clash
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='custom_user_permissions_set',  # Custom related_name to avoid clash
        blank=True
    )

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('Never married', 'Never married'),
        ('Widowed', 'Widowed'),
        ('Annulled', 'Annulled'),
        ('Separated', 'Separated'),
        ('Divorced', 'Divorced'),
    ]
    
    WEDDING_TIMELINE_CHOICES = [
        ('Within 3 years', 'Within 3 years'),
        ('Immediately', 'Immediately'),
        ('Within a year', 'Within a year'),
        ('With a year', 'With a year'),
        ('Within 3+ years', 'Within 3+ years'),
    ]
    
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    interests = models.JSONField()  # assuming you want a list of interests
    marital_status = models.CharField(max_length=50)
    wedding_timeline = models.CharField(max_length=50)
    profession = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
