from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone

TEMPLATES = (
  ('P', 'Personal'),
  ('T', 'Travel'),
  ('H', 'Wellness'),
  ('W', 'Work'),
)

WEATHER_TYPES = (
('S', 'Sunny ☀️'),
('C', 'Cloudy ☁️'),
('R', 'Rainy 🌧️'),
('T', 'Thunderstorm ⛈️'),
('N', 'Snowy ❄️'),
('W', 'Windy 🌬️'),
('F', 'Foggy 🌫️'),
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
    return f"journal.id: {self.id}, user {self.user.id}: {self.user},  name: '{self.name}', template: {self.get_template_display()}"
  
  def get_absolute_url(self):
    return reverse('journals_index')
  
  def has_entries(self):
    return self.entry_set.exists()
  
  def is_empty(self):
    empty = not self.entry_set.exists() and not self.travel_set.exists()
    return empty
  
  def is_travel(self):
    return self.template == 'T'
  
  def count(self):
    if self.is_travel():
      return self.travel_set.count()
    else:
      return self.entry_set.count() 

  



class Entry(models.Model):
  title = models.CharField(max_length=50)
  date = models.DateField()
  body = models.CharField(max_length=1000)
  notes = models.CharField(max_length=300)
  mood_tracker = models.CharField(max_length=25)
  journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

  def __str__(self):
    return f"journal_id: {self.journal.id}, user {self.journal.user.id}: {self.journal.user} , '{self.title}'"
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'journal_id': self.journal_id})
  


class Travel(models.Model):
  title = models.CharField(max_length=50)
  date = models.DateField()
  body = models.CharField(max_length=1000)
  notes = models.CharField(max_length=300)
  mood_tracker = models.CharField(max_length=25)
  location = models.CharField(max_length=50)
  food = models.CharField(max_length=50)
  weather = models.CharField(
	max_length=1,
	choices=WEATHER_TYPES,
	default=WEATHER_TYPES[0][0]
)
  created_at = models.DateField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

  class Meta:
    ordering = ['-updated_at']

  def __str__(self):
    return f"journal_id: {self.journal.id}, user {self.journal.user.id}: {self.journal.user} , template: {self.journal.template}, '{self.title}'"
  
  def weather_display(self):
    return self.get_weather_display()
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'journal_id': self.journal_id})