from django import forms

from app.models import Employee


class TableForm(forms.Form):
    id = forms.CharField(max_length=50, required=False)
    full_name = forms.CharField(max_length=50, required=False)
    position = forms.CharField(max_length=50, required=False)
    hire_date = forms.DateField()
    email = forms.CharField(max_length=50, required=False)

    id.widget.attrs.update({"class": "form-control shadow-none"})
    full_name.widget.attrs.update({"class": "form-control shadow-none"})
    position.widget.attrs.update({"class": "form-control shadow-none"})
    hire_date.widget.attrs.update({"class": "form-control shadow-none"})
    email.widget.attrs.update({"class": "form-control shadow-none"})


class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["full_name", "position", "hire_date", "email", "parent"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Full name"}
            ),
            "position": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Position"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "hire_date": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Hire date"}
            ),
            "parent": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Chief id"}
            ),
        }
