from django.db import models

from datetime import date
# Create your models here.
class FilesUpload(models.Model):
    file = models.FileField()
    date = models.DateField(default=date.today())
