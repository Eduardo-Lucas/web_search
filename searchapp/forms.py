from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
