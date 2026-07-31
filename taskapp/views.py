from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Attendance
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from django.db.models.functions import ExtractMonth
from .forms import EmployeeForm, AttendanceForm, UserUpdateForm


@login_required(login_url='login')
def employee_list(request):
    employees = Employee.objects.all()

    search = request.GET.get("search")
    department = request.GET.get("department")

    # Search
    if search:
        employees = employees.filter(name__icontains=search)

    # Department Filter
    if department:
        employees = employees.filter(department=department)

    # Dashboard Counts (Pagination se PEHLE)
    total_employees = employees.count()
    it_count = employees.filter(department="IT").count()
    hr_count = employees.filter(department="HR").count()
    sales_count = employees.filter(department="sales").count()

    # Recent Employees
    recent_employees = Employee.objects.order_by("-created_at")[:5]

    # Monthly Joining Data
    monthly = Employee.objects.annotate(
        month=ExtractMonth("created_at")
    ).values("month").annotate(
        total=Count("id")
    ).order_by("month")

    months = []
    totals = []

    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar",
        4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep",
        10: "Oct", 11: "Nov", 12: "Dec"
    }

    for m in monthly:
        months.append(month_names.get(m["month"], ""))
        totals.append(m["total"])

    # Pagination (Sabse Last)
    paginator = Paginator(employees, 5)
    page_number = request.GET.get("page")
    employees = paginator.get_page(page_number)

    context = {
        "employees": employees,
        "total_employees": total_employees,
        "it_count": it_count,
        "hr_count": hr_count,
        "sales_count": sales_count,
        "months": months,
        "totals": totals,
        "search": search,
        "department": department,
        "recent_employees": recent_employees,
    }

    return render(request, "employee_list.html", context)

@login_required(login_url='login')
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee Added Successfully!")
            return redirect("employee_list")

    else:
        form = EmployeeForm()

    return render(request, "add_employee.html", {"form": form})

@login_required(login_url='login')
def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee Updated Successfully!")
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, "edit_employee.html",{
        "form": form,
        "employee": employee
        })
    
@login_required(login_url='login')
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee Deleted Successfully!")
        return redirect('employee_list')

    return render(request, 'delete_employee.html', {'employee': employee})

@login_required(login_url='login')
def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'employee_detail.html', {'employee': employee})

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("employee_list")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url='login')
def export_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'Department', 'Designation'])

    # Search aur Department Filter
    employees = Employee.objects.all()

    search = request.GET.get("search")
    department = request.GET.get("department")

    if search:
        employees = employees.filter(name__icontains=search)

    if department:
        employees = employees.filter(department=department)

    # Excel me data likho
    for employee in employees:
        writer.writerow([
            employee.name,
            employee.email,
            employee.phone,
            employee.department,
            employee.designation,
        ])

    return response

@login_required(login_url='login')
def export_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employees.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Employee Report")

    y = 760

    employees = Employee.objects.all()

    p.setFont("Helvetica", 11)

    for emp in employees:

        p.drawString(
            50,
            y,
            f"{emp.name} | {emp.email} | {emp.department}"
        )

        y -= 20

        if y < 40:
            p.showPage()
            y = 800

    p.save()

    return response

@login_required(login_url='login')
def profile(request):
    return render(request, "profile.html")


@login_required(login_url='login')
def edit_profile(request):

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "edit_profile.html", {"form": form})


@login_required(login_url='login')
def attendance_list(request):

    attendance = Attendance.objects.all().order_by("-date")

    employee = request.GET.get("employee")
    status = request.GET.get("status")
    date = request.GET.get("date")

    if employee:
        attendance = attendance.filter(employee__name__icontains=employee)

    if status:
        attendance = attendance.filter(status=status)

    if date:
        attendance = attendance.filter(date=date)
        
    total_attendance = attendance.count()

    present_count = attendance.filter(status="Present").count()

    absent_count = attendance.filter(status="Absent").count()

    if request.method == "POST":
        form = AttendanceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("attendance")

    else:
        form = AttendanceForm()

    context = {
        "form": form,
        "attendance": attendance,
        "employee": employee,
        "status": status,
        "date": date,  
    "total_attendance": total_attendance,
    "present_count": present_count,
    "absent_count": absent_count,
    }

    return render(request, "attendance.html", context)


@login_required(login_url='login')
def edit_attendance(request, id):

    attendance = get_object_or_404(Attendance, id=id)

    if request.method == "POST":

        form = AttendanceForm(request.POST, instance=attendance)

        if form.is_valid():
            form.save()
            return redirect("attendance")

    else:
        form = AttendanceForm(instance=attendance)

    return render(request, "edit_attendance.html", {
        "form": form
    })


@login_required(login_url='login')
def delete_attendance(request, id):

    attendance = get_object_or_404(Attendance, id=id)

    if request.method == "POST":
        attendance.delete()
        return redirect("attendance")

    return render(request, "delete_attendance.html", {
        "attendance": attendance
    })
    
@login_required(login_url='login')
def attendance_excel(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Employee",
        "Date",
        "Status"
    ])

    attendance = Attendance.objects.all()

    for a in attendance:

        writer.writerow([
            a.employee.name,
            a.date,
            a.status
        ])

    return response

@login_required(login_url='login')
def attendance_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="attendance.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "Attendance Report")

    y = 760

    attendance = Attendance.objects.all()

    p.setFont("Helvetica", 12)

    for a in attendance:

        p.drawString(
            50,
            y,
            f"{a.employee.name} | {a.date} | {a.status}"
        )

        y -= 25

        if y < 50:
            p.showPage()
            y = 800

    p.save()

    return response