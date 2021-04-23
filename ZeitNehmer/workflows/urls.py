from django.urls import path
from . import views

from workflows.views import WorkflowsListView

urlpatterns = [
    path('<username>/workflows/', WorkflowsListView.as_view(), name='Workflows'),
    path('<username>/workflows/create/', views.workflowsCreation, name='creation'),
    path('<username>/workflows/<int:pk>/update/', views.WorkflowUpdate.as_view(), name='update_workflow'),
    path('<username>/workflows/<int:pk>/delete/', views.WorkflowDelete.as_view(), name='delete_workflow')
]
