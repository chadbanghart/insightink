from django.forms import ModelForm
from .models import Journal


class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'template']
        
