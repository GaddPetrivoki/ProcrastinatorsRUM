from django.urls import path
from . import views

from workflows.views import WorkflowsListView, TeamsWorkflowsListView

urlpatterns = [
    path('<username>/workflows/', WorkflowsListView.as_view(), name='Workflows'),
    path('<username>/workflows/create/', views.workflowsCreation, name='creation'),
    path('<username>/workflows/<int:pk>/update/', views.WorkflowUpdate.as_view(), name='update_workflow'),
    path('<username>/workflows/<int:pk>/delete/', views.WorkflowDelete.as_view(), name='delete_workflow'),
    #TEAMS
    path('<username>/teams/', views.teamsView, name='teams'),
    path('<username>/teams/create', views.teamsCreate, name='teams_create'),

    #TEAMS' WORKFLOWS
    path('<username>/teams/<int:pk>/', TeamsWorkflowsListView.as_view(), name='teams_workflows'),
    path('<username>/teams/manage/', views.manageMember, name='teams_manage'),
]
