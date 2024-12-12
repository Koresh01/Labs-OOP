from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
# Create your models here.
class Good(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Token(models.Model):
    token = models.CharField(max_length=36, unique=True)
    def __str__(self):
        return self.token