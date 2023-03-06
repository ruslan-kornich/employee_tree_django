from django.shortcuts import render

from app.models import Employee


# Create your views here.


def employee_tree(request):
    employees = Employee.objects.all()
    count_all = Employee.objects.count()
    data = {"employees": employees, "count_all": count_all}
    return render(request, template_name="app/employee_tree.html", context=data)
