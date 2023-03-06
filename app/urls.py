from django.urls import path

from app.views import *

urlpatterns = [
    path("", employee_tree, name="employee-tree"),
]
