from django.db import models
from django.urls import reverse
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

  def __str__(self):
    return f"{self.get_template_display()} {self.name} {self.id}"
  
  def get_absolute_url(self):
    return reverse('journals_index')
  
  def has_entries(self):
    return self.entry_set.count() > 0
  
  def has_no_entries(self):
    return self.entry_set.count() == 0

class Entry(models.Model):
  title = models.CharField(max_length=50)
  date = models.DateField()
  body = models.CharField(max_length=1000)
  notes = models.CharField(max_length=300)
  mood_tracker = models.CharField(max_length=25)
  journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.title}'