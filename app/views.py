from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms import TableForm, EmployeesForm
from app.models import Employee
from app.utiils import last_sort_by


# Create your views here.


def employee_tree(request):
    employees = Employee.objects.all()
    count_all = Employee.objects.count()
    data = {"employees": employees, "count_all": count_all}
    return render(request, template_name="app/employee_tree.html", context=data)


def employee_table(request):
    if request.user.is_authenticated:
        last_sort_by("id")
        employees = Employee.objects.order_by("id").all()  # id sorting
        pagination = Paginator(employees, 50).get_page(1)
        table_form = TableForm()
        employees_form = EmployeesForm()
        form_names = zip(
            table_form, ["id", "Full name", "Position", "Hire date", "Email"]
        )

        data = {
            "employees": pagination,
            "form_names": form_names,
            "form": table_form,
            "employees_form": employees_form,
            "page": pagination,
        }
        return render(request, template_name="app/employee_table.html", context=data)
    else:
        template_name = "app/login.html"
        data = {"text": "You are not authorized."}
        return render(request, template_name, context=data)


def logout_manager(request):
    logout(request)
    data = {"text": "You’ve Been Logged Out"}
    return render(request, template_name="app/login.html", context=data)


def login_manager(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("employee-table"))  # success page
        else:
            data = {"text": "There is no such user"}
            return render(request, template_name="app/login.html", context=data)
    else:
        data = {"text": "You can authorize."}
        return render(request, template_name="app/not_auth.html", context=data)
