from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Journal(models.Model):
  name = models.CharField(max_length=50)
  date = models.DateField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)