from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    
    photo = models.ImageField(upload_to="employees/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
  

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    STATUS = (
        ("Present", "Present"),
        ("Absent", "Absent"),
    )

    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"