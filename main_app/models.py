from django.db import models
from datetime import date
from django.contrib.auth.models import User

TEMPLATES = (
  ('P', 'Personal'),
  ('T', 'Travel'),
  ('H', 'Wellness'),
  ('W', 'Work'),
)

# Create your models here.
class Journal(models.Model):
  name = models.CharField(max_length=50)
  template = models.CharField(
	max_length=1,
	choices=TEMPLATES,
	default=TEMPLATES[0][0]
)

  user = models.ForeignKey(User, on_delete=models.CASCADE)