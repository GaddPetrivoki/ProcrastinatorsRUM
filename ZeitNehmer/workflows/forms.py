from .models import Workflows
from django import forms
from django.forms import ModelForm

class WorkflowsForm(forms.ModelForm):
    class Meta:
        model = Workflows
        fields = ['name', 'description', 'dueDate', 'priority']
