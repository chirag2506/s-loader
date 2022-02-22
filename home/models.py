from django.db import models

# Create your models here.
class User(models.Model):
    name = models.TextField()
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True, primary_key=True
    )
    password = models.TextField()
