from datetime import date
from django import forms
from django.forms import ModelForm, DateInput, TimeInput, TextInput
from .models import Meeting

class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ["title", "date", "start_time", "duration", "room"]
        widgets = {
            'date': DateInput(attrs={"type": "date"}),
            'start_time': TimeInput(attrs={"type": "time"}),
            'duration': TextInput(attrs={"type": "number", "min": "1", "max": "24"}),
        }

    def clean_date(self):
        d = self.cleaned_data.get("date")
        if d < date.today():
            raise forms.ValidationError("Meetings cannot be in the past")
        return d