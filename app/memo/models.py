from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=64)

class Memo(models.Model):
    index = models.IntegerField()
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=100)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
