from django.forms import ModelForm

from .models import Championship

class GameForm(ModelForm):
    class Meta:
        model = Championship
        fields = ['title']
        labels = {'title': 'Title'}
