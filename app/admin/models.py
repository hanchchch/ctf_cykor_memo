from django.db import models

from memo.models import User

class Admin(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Report(models.Model):
    index = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=100)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
