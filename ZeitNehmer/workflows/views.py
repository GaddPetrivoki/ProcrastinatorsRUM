from django.shortcuts import render, redirect
# Create your views here.
from django_tables2 import SingleTableView
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from .models import Workflows
from .tables import WorkflowsTable
from .forms import WorkflowsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django import forms
class WorkflowsListView(LoginRequiredMixin, SingleTableView):
    def get_queryset(self):
        return Workflows.objects.filter(owner=self.request.user.id)
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Workflows

    table_class = WorkflowsTable
    template_name = 'index.html'


def workflowsCreation(request, username):
    form = WorkflowsForm()

    if request.method == 'POST':
        form = WorkflowsForm(request.POST)
        if form.is_valid():
            #This is done so there is no "Integrity Error"
            workflow = form.save(commit=False)
            workflow.owner = request.user
            workflow.save()
            messages.success(request, f'New Workflow Added!')
            return redirect('Workflows', username=username)
    return render(request, 'new_workflow.html', {'form': form})

class WorkflowUpdate(UpdateView):
    model = Workflows
    form_class = WorkflowsForm
    template_name = "updateWorkflow.html"

    success_url = reverse_lazy('Workflows', args=['request.user'])

class WorkflowDelete(DeleteView):
    model = Workflows
    success_url = reverse_lazy('Workflows', args=['request.user'])
    template_name = 'deleteWorkflow.html'

def workflowSingleView(request, pk):
    results = Workflows.objects.get(pk=pk)
    context = {'workflows': results}
    return render(request,'workflowView.html', context)
