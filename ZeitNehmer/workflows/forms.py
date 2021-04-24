from .models import Workflows, Teams
from django import forms
from django.forms import ModelForm

class WorkflowsForm(forms.ModelForm):
    class Meta:
        model = Workflows
        fields = ['name', 'description', 'dueDate', 'priority']
        widgets = {
            'dueDate': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control',
            'placeholder': 'Select a date',
            'type': 'date'
            }),
        }

class TeamsForm(forms.ModelForm):
    class Meta:
        model = Teams
        fields = ['name', 'description']
