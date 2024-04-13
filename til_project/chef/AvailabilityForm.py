from django import forms
from django.utils.html import escape
from .models import Availability

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_time', 'end_time', 'date', 'vacancies', 'filled_seats', 'additional_info']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input-field'}),
            'start_time': forms.TimeInput(attrs={'class': 'input-field'}),
            'end_time': forms.TimeInput(attrs={'class': 'input-field'}),
            'vacancies': forms.NumberInput(attrs={'class': 'input-field'}),
            'filled_seats': forms.NumberInput(attrs={'class': 'input-field'}),
            'additional_info': forms.TextInput(attrs={'class': 'input-field'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['start_time'] = escape(cleaned_data.get('start_time'))
        cleaned_data['end_time'] = escape(cleaned_data.get('end_time'))
        cleaned_data['date'] = escape(cleaned_data.get('date'))
        cleaned_data['vacancies'] = escape(cleaned_data.get('vacancies'))
        cleaned_data['filled_seats'] = escape(cleaned_data.get('filled_seats'))
        cleaned_data['additional_info'] = escape(cleaned_data.get('additional_info'))
        return cleaned_data
