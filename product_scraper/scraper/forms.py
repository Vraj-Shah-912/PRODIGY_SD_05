from django import forms

class ScraperForm(forms.Form):
    url = forms.URLField(label='Product URL', max_length=200)
