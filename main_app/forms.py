from django.forms import ModelForm
from .models import Journal, Entry, Travel, Wellness


class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'template']

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'body', 'date', 'mood', 'notes']

class TravelForm(ModelForm):
    class Meta:
        model = Travel
        fields = ['title', 'body', 'date', 'mood', 'location', 'food', 'weather', 'notes']

class WellnessForm(ModelForm):
    class Meta:
        model = Wellness
        fields = ['title', 'body', 'date', 'mood', 'affirmation', 'sleep', 'food', 'notes']        
