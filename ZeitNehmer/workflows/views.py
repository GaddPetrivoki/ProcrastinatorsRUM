from django.shortcuts import render, redirect
# Create your views here.
from django_tables2 import SingleTableView
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from .models import Workflows, Teams
from .tables import WorkflowsTable
from .forms import WorkflowsForm, TeamsForm, addMemberForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.models import User
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
    form.fields['members'].queryset = User.objects.exclude(username = request.user)
    print(form.fields['members'].queryset)
    if request.method == 'POST':
        form = TeamsForm(request.POST)
        if form.is_valid():
            #This is done so there is no "Integrity Error"
            team = form.save(commit=False)
            team.save()
            team.members.add(request.user)

            for members in request.POST.getlist('members'):
                team.members.add(members)

            messages.success(request, f'New Workflow Added!')
            return redirect('teams', username=username)

    return render(request, 'teams/create_teams.html', {'form': form})

class TeamsWorkflowsListView(LoginRequiredMixin, SingleTableView):
    def get_queryset(self):
        self.request.session['team'] = self.kwargs['pk']
        return Workflows.objects.filter(owner=self.request.user.id, team = self.request.session['team'] )

    def get_context_data(self,**kwargs):
        self.request.session['team'] = self.kwargs['pk']
        context = super(TeamsWorkflowsListView,self).get_context_data(**kwargs)
        context['team'] = Teams.objects.filter(id = self.request.session['team'] )[0]
        return context
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Workflows

    table_class = WorkflowsTable
    template_name = 'workflows/index.html'

def manageMember(request, username):
    queryset = Teams.objects.filter(id = request.session['team'])
    team = queryset[0]
    context = team.members.all()
    if request.method == 'POST':
        if request.POST.get('member') == None:
            team.members.remove(request.POST.get('delete_member'))
        else:
            newMember = User.objects.filter(username=request.POST.get('member'))

            if not newMember:
                 messages.info(request, 'Member does not exist!')
            else:
                team.members.add(User.objects.filter(username=request.POST.get('member'))[0])

    return render(request, 'teams/manage_members.html', {'members': context, 'team': team})
