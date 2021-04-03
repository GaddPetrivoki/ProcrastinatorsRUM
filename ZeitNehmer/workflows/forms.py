from .models import Workflows
from django.forms import ModelForm

class WorkflowsForm(ModelForm):
    class Meta:
        model = Workflows
        fields = ['name', 'description', 'dueDate', 'priority']
