from django.shortcuts import render, redirect
# Create your views here.
from django_tables2 import SingleTableView
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from .models import Workflows, Teams
from .tables import WorkflowsTable
from .forms import WorkflowsForm, TeamsForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.http import HttpResponseRedirect

#Personal
class WorkflowsListView(LoginRequiredMixin, SingleTableView):
    def get_queryset(self):

        self.request.session['team'] = None
        print(self.request.session['team'])
        self.request.session['prev_url'] = self.request.get_full_path()
        return Workflows.objects.filter(owner=self.request.user.id)
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Workflows

    table_class = WorkflowsTable
    template_name = 'workflows/index.html'

def workflowsCreation(request, username):
    form = WorkflowsForm()

    print(request.session['prev_url'])
    if request.method == 'POST':

        form = WorkflowsForm(request.POST)
        if form.is_valid():
            if request.session['team'] == None:
            #This is done so there is no "Integrity Error"
                workflow = form.save(commit=False)
                workflow.owner = request.user
                workflow.save()
                return redirect("Workflows", username=username)
            else:
                workflow = form.save(commit=False)
                workflow.owner = request.user
                workflow.team = Teams.objects.filter(id=request.session['team'])[0]
                workflow.save()
                return redirect('teams_workflows', username=username, pk=request.session['team'])

    return render(request, 'workflows/new_workflow.html', {'form': form})

class WorkflowUpdate(UpdateView):
    model = Workflows
    form_class = WorkflowsForm
    template_name = "workflows/updateWorkflow.html"
    def get_success_url(self, **kwargs):
        print(self.request.POST.get('team'))
        if self.request.session['team'] == None:
            return reverse_lazy('Workflows', args=[self.request.user])
        else:
            return reverse_lazy('teams_workflows', args=[self.request.user, self.request.session['team']])

class WorkflowDelete(DeleteView):
    model = Workflows
    template_name = 'workflows/deleteWorkflow.html'
    def get_success_url(self, **kwargs):
        if self.request.session['team'] == None:
            return reverse_lazy('Workflows', args=[self.request.user])
        else:
            return reverse_lazy('teams_workflows', args=[self.request.user, self.request.session['team']])


#Teams

def teamsView(request, username):
    teams = Teams.objects.filter(members= request.user.id)
    return render(request, 'teams/teams.html', {'teams': teams})

def teamsCreate(request, username):
    form = TeamsForm()

    if request.method == 'POST':
        form = TeamsForm(request.POST)
        if form.is_valid():
            #This is done so there is no "Integrity Error"
            team = form.save(commit=False)
            team.members = request.user
            team.save()
            messages.success(request, f'New Workflow Added!')
            return redirect('teams', username=username)

    return render(request, 'teams/create_teams.html', {'form': form})

class TeamsWorkflowsListView(LoginRequiredMixin, SingleTableView):
    def get_queryset(self):
        self.request.session['team'] = self.kwargs['pk']
        return Workflows.objects.filter(owner=self.request.user.id, team = self.request.session['team'] )
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Workflows

    table_class = WorkflowsTable
    template_name = 'workflows/index.html'
