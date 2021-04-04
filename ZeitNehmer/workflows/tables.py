import django_tables2 as tables
from .models import Workflows
from django.utils.safestring import mark_safe

class CustomTemplateColumn(tables.TemplateColumn):
   def render(self, record, table, value, bound_column, **kwargs):
        return super(CustomTemplateColumn, self).render(record, table, value, bound_column, **kwargs)




class WorkflowsTable(tables.Table):
    updateButton = '<a href="/workflows/{{record.id}}/update" class="btn btn-primary">UPDATE</a>'
    updateWorkflow = CustomTemplateColumn(updateButton)

    viewButton = '<a href="/workflows/{{record.id}}/delete" class="btn btn-danger">DELETE</a>'
    viewWorkflow = CustomTemplateColumn(viewButton)

    dueDate = tables.DateTimeColumn(format ='M d Y')



    class Meta:
        model = Workflows
        template_name = "django_tables2/bootstrap.html"
        fields =  ('name', 'description', 'dueDate', 'priority' )
