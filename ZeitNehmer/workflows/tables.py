import django_tables2 as tables
from .models import Workflows

class CustomTemplateColumn(tables.TemplateColumn):
   def render(self, record, table, value, bound_column, **kwargs):
        return super(CustomTemplateColumn, self).render(record, table, value, bound_column, **kwargs)


class WorkflowsTable(tables.Table):
    viewButton = '<a href="/workflows/{{record.id}}/">VIEW</a>'
    viewWorkflow = CustomTemplateColumn(viewButton)

    dueDate = tables.DateTimeColumn(format ='M d Y')
    
    class Meta:
        model = Workflows
        template_name = "django_tables2/bootstrap.html"

        fields = ("name", "description", 'dueDate', "priority" )
