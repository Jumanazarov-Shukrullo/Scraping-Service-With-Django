from django import forms
from scraping.models import Language, City


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Language'
    )