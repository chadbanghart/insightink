from django.forms import ModelForm
from .models import Journal, Entry, Travel


class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'template']

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'body', 'date', 'mood_tracker', 'notes']

class TravelForm(ModelForm):
    class Meta:
        model = Travel
        fields = ['title', 'body', 'date', 'mood_tracker','location', 'food', 'weather', 'notes']
