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
    form = WorkflowsForm()
    if request.method == 'POST':
        form = WorkflowsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'New Workflow Added!')
            return redirect('Workflows')
    return render(request, 'new_workflow.html', {'form': form})
    # else:
    #     form = WorkflowsForm()
    #
    #     return render(request, 'new_workflow.html', {'form': form})
