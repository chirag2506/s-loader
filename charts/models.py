from django.db import models
from django.conf import settings
from datetime import date
# from django.contrib.auth.models import User
from home.models import User
from sloader.middleware import get_current_user

#
class StoreData(models.Model):
    # def for_user(self, user):
    #     return self.get_query_set().filter(naam=user)
    # a=get_current_user()
    # naam= models.CharField(max_length=50, default=get_current_user)
    date = models.DateField(default=date.today())
    # nof = models.IntegerField(default=0)
    # filename = models.CharField(max_length=50)
# class HourRecord(models.Model):
#     #Managers
#     objects = StoreData()
