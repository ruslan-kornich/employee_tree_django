from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Employee(MPTTModel):
    class MPTTMeta:
        order_insertion_by = ["full_name"]  # By which field to sort children's in tree

    full_name = models.CharField(max_length=255, db_index=True)
    position = models.CharField(max_length=255, db_index=True)
    hire_date = models.DateField()
    email = models.EmailField(max_length=254)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.full_name
