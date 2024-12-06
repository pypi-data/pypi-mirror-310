from django.shortcuts import render
from bloomerp.utils.router import BloomerpRouter
from .models import Employee
from bloomerp.views.mixins import HtmxMixin
from django.views import View

# Create your views here.

router = BloomerpRouter()

@router.bloomerp_route(
    path='send-emails',
    name='Send Emails',
    description='Send emails to employees',
    route_type='list',
    url_name='send_emails',
    models=Employee
)
class SendEmailsView(HtmxMixin, View):
    template_name = 'email_employees.html'
    model = Employee


    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        employee_list = Employee.objects.all()
        context['employee_list'] = employee_list
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        employee_list = Employee.objects.all()
        context['employee_list'] = employee_list
        return render(request, self.template_name, context)
        
    def get_context_data(self, **kwargs):
        return {}