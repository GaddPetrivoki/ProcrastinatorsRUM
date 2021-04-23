import django_tables2 as tables
from .models import Workflows
from django.utils.safestring import mark_safe

class CustomTemplateColumn(tables.TemplateColumn):
   def render(self, record, table, value, bound_column, **kwargs):
        return super(CustomTemplateColumn, self).render(record, table, value, bound_column, **kwargs)




class WorkflowsTable(tables.Table):
    updateButton = '<a href="{% url \'update_workflow\' request.user record.id %}" class="btn btn-primary">UPDATE</a>'
    updateWorkflow = CustomTemplateColumn(updateButton, verbose_name=" ")

    viewButton = '<a href="{% url \'delete_workflow\' request.user record.id %}" class="btn btn-danger">DELETE</a>'
    viewWorkflow = CustomTemplateColumn(viewButton, verbose_name=" ")

    dueDate = tables.DateTimeColumn(format ='M d Y', verbose_name="Due Date")




    class Meta:
        model = Workflows
        template_name = "django_tables2/bootstrap.html"
        fields =  ('name', 'description', 'dueDate', 'priority' )
