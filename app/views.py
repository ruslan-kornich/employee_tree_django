from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms import TableForm, EmployeesForm
from app.models import Employee, Department
from app.utils import last_sort_by


# Create your views here.


def employee_tree(request):
    return render(request, template_name="app/employee_tree.html")


def employee_tree_api(request, dip=None):
    if dip is None:
        return employee_tree_root(request)
    departments = Department.objects.filter(parent=dip)
    result = {}
    if departments.count() > 0:
        result["departments"] = []
        for department in departments:
            result["departments"].append({"id": department.id, "name": department.name})
    try:
        employees = Employee.objects.filter(
            department=Department.objects.get(id=dip)
        ).order_by("name")
    except Department.DoesNotExist:
        employees = None
    if employees is not None and employees.count() > 0:
        result["employees"] = []
        for employee in employees:
            result["employees"].append({"id": employee.id, "name": employee.name})
    return JsonResponse(result)


def employee_tree_root(request):
    departments = Department.objects.filter(level=0)
    result = {}
    if departments.count() > 0:
        result["departments"] = []
        for department in departments:
            result["departments"].append(
                {
                    "id": department.id,
                    "name": department.name,
                    "child": not department.is_leaf_node(),
                }
            )
    return JsonResponse(result)


def employee_tree_api_detail(request, eip):
    try:
        detail = Employee.objects.get(id=eip)
    except Employee.DoesNotExist:
        detail = None
    result = {}
    if detail is not None:
        result["detail"] = [
            f"ПІБ: {detail.name}",
            f"Посада: {detail.position}",
            f'Дата прийому: {detail.hire_date.strftime("%d.%m.%Y")}',
            f"Email: {detail.email}",
        ]
    return JsonResponse(result)


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
        return render(request, template_name="app/login.html", context=data)
