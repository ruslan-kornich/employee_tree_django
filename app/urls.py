from django.urls import path

from app import views

urlpatterns = [
    path("", views.employee_tree, name="employee-tree"),
    path("table/", views.employee_table, name="employee-table"),
    path("table/login/", views.login_manager, name="login"),
    path("logout/", views.logout, name="logout"),
]
