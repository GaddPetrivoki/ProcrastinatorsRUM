import django_tables2 as tables
from .models import Workflows

class WorkflowsTable(tables.Table):
    class Meta:
        model = Workflows
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "description", "Due Date", "Priority" )
