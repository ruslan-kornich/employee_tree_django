from django.http import JsonResponse

lsb = "id"  # global variable last sort_by


def last_sort_by(sort_by=""):
    """Remember last sort"""
    global lsb
    if sort_by:
        lsb = sort_by
    return lsb


def json_data_table(queryset, server_response):
    li = {"q": [], "s_res": server_response, "p": []}  # packing data for json
    for emp in queryset:
        li["q"].append(
            {
                "id": emp.id,
                "nm": emp.name,
                "pos": emp.position,
                "dt": emp.hire_date,
                "sl": emp.email,
                "par": emp.department_id,
            }
        )
    li["p"].append(
        {
            "has_prev": queryset.has_previous(),
            "has_next": queryset.has_next(),
            "num_pages": queryset.paginator.num_pages,
            "number": queryset.number,
            "count": queryset.paginator.count,
        }
    )
    print(li["p"])
    return JsonResponse(li)
