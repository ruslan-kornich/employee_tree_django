from django import forms

from app.models import Employee


class TableForm(forms.Form):
    id = forms.CharField(max_length=50, required=False)
    name = forms.CharField(max_length=50, required=False)
    position = forms.CharField(max_length=50, required=False)
    hire_date = forms.CharField(max_length=50, required=False)
    email = forms.CharField(max_length=50, required=False)

    id.widget.attrs.update({'class': 'form-control shadow-none'})
    name.widget.attrs.update({'class': 'form-control shadow-none'})
    position.widget.attrs.update({'class': 'form-control shadow-none'})
    hire_date.widget.attrs.update({'class': 'form-control shadow-none'})
    email.widget.attrs.update({'class': 'form-control shadow-none'})


class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'email', 'hire_date', "department"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Hire Date'}),
            'department': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number Department'})

        }
