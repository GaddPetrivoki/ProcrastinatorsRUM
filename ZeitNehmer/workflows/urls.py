from django.urls import path
from . import views

from workflows.views import WorkflowsListView

urlpatterns = [
    path('', WorkflowsListView.as_view(), name='Workflows'),
    path('create/', views.workflowsCreation, name='creation')
]
