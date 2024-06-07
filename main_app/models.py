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

MOODS = (
  ('H', 'Happy 😊'),
  ('S', 'Sad 😢'),
  ('C', 'Content 😌'),
  ('A', 'Angry 😡'),
  ('T', 'Tired 🥱'),
  ('X', 'Anxious 😰'),
  ('K', 'Sick 🤒'),
)

# Create your models here.
class Journal(models.Model):
  name = models.CharField(max_length=50)
  template = models.CharField(
	max_length=1,
	choices=TEMPLATES,
	default=TEMPLATES[0][0]
  )
  created_at = models.DateField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    ordering = ['-updated_at']

  def __str__(self):
    return f"journal.id: {self.id}, user {self.user.id}: {self.user},  name: '{self.name}', template: {self.get_template_display()}"
  
  def get_absolute_url(self):
    return reverse('journals_index')
  
  def has_entries(self):
    return self.entry_set.exists()
  
  def is_empty(self):
    empty = not self.entry_set.exists() and not self.travel_set.exists() and not self.wellness_set.exists()
    return empty
  
  def is_travel(self):
    return self.template == 'T'
  
  def is_wellness(self):
    return self.template == 'H'
  
  def count(self):
    if self.is_travel():
      return self.travel_set.count()
    elif self.is_wellness():
      return self.wellness_set.count()
    else:
      return self.entry_set.count() 



class Entry(models.Model):
  title = models.CharField(max_length=50)
  date = models.DateField()
  body = models.CharField(max_length=1000)
  notes = models.CharField(max_length=300)
  mood = models.CharField(
	max_length=1,
	choices=MOODS,
	default=MOODS[0][0]
  )

  created_at = models.DateField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

  class Meta:
    ordering = ['-updated_at']

  def __str__(self):
    return f"journal_id: {self.journal.id}, user {self.journal.user.id}: {self.journal.user} , '{self.title}'"
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'journal_id': self.journal_id})
  
  def mood_display(self):
    return self.get_mood_display()
  


class Travel(models.Model):
  title = models.CharField(max_length=50)
  date = models.DateField()
  body = models.CharField(max_length=1000)
  notes = models.CharField(max_length=300)
  mood = models.CharField(
	max_length=1,
	choices=MOODS,
	default=MOODS[0][0]
  )
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
  
  def mood_display(self):
    return self.get_mood_display()
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'journal_id': self.journal_id})
  


class Wellness(models.Model):
  title = models.CharField(max_length=50)
  date = models.DateField()
  body = models.TextField(max_length=1000)
  notes = models.TextField(max_length=300)
  affirmation = models.TextField(max_length=200)
  food = models.CharField(max_length=50)
  sleep = models.IntegerField()
  mood = models.CharField(
	max_length=1,
	choices=MOODS,
	default=MOODS[0][0]
  )

  created_at = models.DateField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

  def mood_display(self):
    return self.get_mood_display()

  def get_absolute_url(self):
    return reverse('detail', kwargs={'journal_id': self.journal_id})
  
  def __str__(self):
    return f"journal_id: {self.journal.id}, user {self.journal.user.id}: {self.journal.user} , template: {self.journal.template}, '{self.title}'"
  
class Photo(models.Model):
    url = models.CharField(max_length=200)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for travel_id: {self.travel_id} @{self.url}"  