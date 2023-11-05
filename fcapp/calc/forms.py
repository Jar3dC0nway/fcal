from django import forms
from django.forms import TextInput


class CalculatorForm(forms.Form):
    number = forms.FloatField(initial=0)
    rate = forms.FloatField(initial=0)
    present_value = forms.FloatField(initial=0)
    payments = forms.FloatField(initial=0)
    future_value = forms.FloatField(initial=0)
    operation = forms.IntegerField(initial=0)
