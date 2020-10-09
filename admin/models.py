from django.db import models

from memo.models import User

class Admin(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)

class Report(models.Model):
    index = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=100)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
