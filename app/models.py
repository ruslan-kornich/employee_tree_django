from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    name = models.CharField("Підрозділ", max_length=50, unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Знаходиться у підрозділі",
    )

    class Meta:
        verbose_name = "Підрозділ"
        verbose_name_plural = "Підрозділи"

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField("ПІБ", max_length=50, blank=False)
    position = models.CharField("Посада", max_length=50, blank=False)
    hire_date = models.DateField("Дата прийому", blank=True, null=True)
    email = models.EmailField("Email", max_length=254, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Співробітника"
        verbose_name_plural = "Співробітники"

    def __str__(self):
        return f"[ID{str(self.id)}] {self.name}"
