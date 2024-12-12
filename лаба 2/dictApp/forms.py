from dictApp.models import *
from django.forms.models import ModelForm

class WordForm(ModelForm):
    class Meta:
        model = Word
        fields = ["word","translation"]
    