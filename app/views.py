from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from app.forms import TableForm, EmployeesForm
from app.models import Employee, Department
from app.utils import last_sort_by, json_data_table


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
            f'Дата прийому: {detail.hire_date.strftime("%d-%m-%Y")}',
            f"Email: {detail.email}",
        ]
    return JsonResponse(result)


def employee_table(request):
    if request.user.is_authenticated:
        last_sort_by("id")
        employees = Employee.objects.order_by("id").all()  # id sorting
        pages = Paginator(employees, 50).get_page(1)
        table_form = TableForm()
        employee_form = EmployeesForm()
        form_names = zip(
            table_form, ["id", "Повне ім'я", "Посада", "Дата найму", "Email"]
        )

        data = {
            "employees": pages,
            "form_names": form_names,
            "form": table_form,
            "employee_form": employee_form,
            "page": pages,
        }
        print(data)
        return render(request, template_name="app/employee_table.html", context=data)

    else:
        data = {"text": "No login"}
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
        data = {"text": "Ви можете авторизуватися"}
        return render(request, template_name="app/login.html", context=data)


@csrf_protect
def ajax_table(request):
    if request.method == "POST" and request.user.is_authenticated:
        server_response = ""
        emps = Employee.objects
        print(request.POST)
        print(request.FILES)

        if "del" in request.POST:
            del_id = int(request.POST["del"])  # deleted object id
            del_obj = emps.get(id=del_id)  # remote object itself

            del_obj.delete()
            server_response = "Запис видалено"
        else:
            server_response = "error"

        if "create" in request.POST:
            bound_form = EmployeesForm(request.POST, request.FILES)
            if bound_form.is_valid():
                bound_form.save()
                server_response = "Створено новий запис"
            else:
                server_response = "Будь ласка, заповніть поля імені та ID департаменту"

        if "update" in request.POST:
            emp_id = request.POST["update"]
            emp = emps.get(id=emp_id)
            bound_form = EmployeesForm(request.POST, request.FILES, instance=emp)
            if bound_form.is_valid():
                bound_form.save()
                server_response = "Запис було оновлено"
            else:
                server_response = "Будь ласка, заповніть поля імені та ID департаменту"

        if "search" in request.POST:  # if search button was pressed
            search = request.POST["search"]  # which field to serch
            emp = eval("emp.filter(" + search + "__icontains=request.POST[search])")

        if "sort_by" in request.POST:  # if sort_by button was pressed
            sort_by = request.POST["sort_by"]  # memorized the sort field

            if sort_by[0] == "-":  # if sort field start with '-'
                search = sort_by[1:]  # delete '-'
            else:
                search = sort_by  # by which field of the model to search

            if request.POST[search]:  # if the searh field is not empty
                emps = eval(
                    "emps.filter(" + search + "__icontains=request.POST[search])"
                )
            emps = emps.order_by(
                sort_by
            ).all()  # Sort by value of the 'sort_by' variable
            last_sort_by(sort_by)
        else:
            emps = emps.order_by(last_sort_by()).all()

        page = int(request.POST["page"])
        p = Paginator(emps, 50)
        p = p.get_page(page)
        return json_data_table(p, server_response)

    return render(request, "404.html")  # if someone tryes to get to the page
