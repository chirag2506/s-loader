from django.db import models
from datetime import date

class StoreData(models.Model):
    naam= models.CharField(max_length=50)
    date = models.DateField(default=date.today())