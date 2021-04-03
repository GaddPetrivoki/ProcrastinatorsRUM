from django.shortcuts import render, redirect
# Create your views here.
from django_tables2 import SingleTableView
from django.contrib import messages

from .models import Workflows
from .tables import WorkflowsTable
from .forms import WorkflowsForm


class WorkflowsListView(SingleTableView):
    model = Workflows
    table_class = WorkflowsTable
    template_name = 'index.html'

def workflowsCreation(request):
    if request.method == 'POST':
        form = WorkflowsForm(request.POST)
        form.save()
        messages.success(request, f'New Workflow Added!')
        return redirect('Workflows')
    else:
        form = WorkflowsForm()

        return render(request, 'new_workflow.html', {'form': form})
