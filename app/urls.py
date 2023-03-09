from django.urls import path

from app import views

urlpatterns = [
    path("", views.employee_tree, name="employee_tree"),
    path("api/get", views.employee_tree_api, name="treeview-api"),
    path("api/get/<int:dip>", views.employee_tree_api, name="treeview-api"),
    path("api/get/root", views.employee_tree_root, name="treeview-api-root"),
    path(
        "api/get/detail/<int:eip>", views.employee_tree_api_detail, name="treeview-api"
    ),
    path("table/", views.employee_table, name="employee-table"),
    path("ajax_table", views.ajax_table),
    path("table/login/", views.login_manager, name="login"),
    path("logout/", views.logout, name="logout"),
]
