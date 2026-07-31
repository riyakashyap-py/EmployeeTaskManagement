from django import forms
from .models import Employee, Attendance
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
            "phone": forms.TextInput(attrs={"class":"form-control"}),
            "department": forms.TextInput(attrs={"class":"form-control"}),
            "designation": forms.TextInput(attrs={"class":"form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class":"form-control"}),
        }
        
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"

        widgets = {
            "employee": forms.Select(attrs={"class":"form-select"}),
            "date": forms.DateInput(attrs={
                "class":"form-control",
                "type":"date"
            }),
            "status": forms.Select(attrs={"class":"form-select"}),
        }