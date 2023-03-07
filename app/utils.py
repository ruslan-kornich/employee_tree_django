lsb = "id"  # global variable last sort_by


def last_sort_by(sort_by=""):
    """Remember last sort"""
    global lsb
    if sort_by:
        lsb = sort_by
    return lsb
