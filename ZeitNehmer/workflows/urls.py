from django.urls import path
from . import views

from workflows.views import WorkflowsListView

urlpatterns = [
    path('', WorkflowsListView.as_view(), name='Workflows'),
    path('create/', views.workflowsCreation, name='creation'),
    path('<int:pk>/', views.workflowSingleView, name='single'),
    path('<int:pk>/update/', views.WorkflowUpdate.as_view(), name='update_workflow'),
    path('<int:pk>/delete/', views.WorkflowDelete.as_view(), name='delete_workflow')
]
