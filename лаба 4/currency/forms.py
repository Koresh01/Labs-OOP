from .models import Currency
from django import forms


class CurrencyForm(forms.ModelForm):
    From = forms.CharField(label="Currency from")
    To = forms.CharField(label="Currency to")
    amount = forms.FloatField(label="Amount")
    class Meta:
        model = Currency
        fields = ['From', 'To']
        widgets = {
            'From': forms.TextInput(attrs={'class': 'form-control', 'name':'from', 'id': '1'}),
            'To': forms.TextInput(attrs={'class': 'form-control', 'name' : 'to','id': '2'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'name': 'ammount', 'id': '3'}),
        }