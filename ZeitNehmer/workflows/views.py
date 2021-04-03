from django.shortcuts import render, redirect
# Create your views here.
from django_tables2 import SingleTableView
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from .models import Workflows
from .tables import WorkflowsTable
from .forms import WorkflowsForm

from django.urls import reverse_lazy

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

class WorkflowUpdate(UpdateView):
    model = Workflows
    fields = ["name", "description", "dueDate", "priority"]
    template_name = "updateWorkflow.html"
    success_url = reverse_lazy('Workflows')

class WorkflowDelete(DeleteView):
    model = Workflows
    success_url = reverse_lazy('Workflows')
    template_name = 'deleteWorkflow.html'

def workflowSingleView(request, pk):
    return render(request,'workflowView.html')
