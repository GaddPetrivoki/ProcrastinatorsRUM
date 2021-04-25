from .models import Workflows, Teams
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
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
        fields = ['name', 'description', 'members']

    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required = False,
    )
class addMemberForm(forms.Form):
    member = forms.CharField(label='Member', max_length=100)
