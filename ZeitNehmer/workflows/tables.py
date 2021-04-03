import django_tables2 as tables
from .models import Workflows

class CustomTemplateColumn(tables.TemplateColumn):
   def render(self, record, table, value, bound_column, **kwargs):
        return super(CustomTemplateColumn, self).render(record, table, value, bound_column, **kwargs)

class WorkflowsTable(tables.Table):
    model = Workflows
    a = Workflows.id
    viewButton = '<a href="/workflows/{{record.id}}/">VIEW</a>'
    viewWorkflow = CustomTemplateColumn(viewButton)
    class Meta:
        model = Workflows
        template_name = "django_tables2/bootstrap.html"

        fields = ("name", "description", "Due Date", "Priority" )
