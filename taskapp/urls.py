from django.urls import path
from . import views

urlpatterns = [

    # Home → Login Page
    path("", views.login_view, name="home"),

    # Dashboard
    path("dashboard/", views.employee_list, name="employee_list"),

    # Employee
    path("add/", views.add_employee, name="add_employee"),
    path("edit/<int:id>/", views.edit_employee, name="edit_employee"),
    path("delete/<int:id>/", views.delete_employee, name="delete_employee"),
    path("employee/<int:id>/", views.employee_detail, name="employee_detail"),

    # Login / Logout
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Export
    path("export/", views.export_excel, name="export_excel"),
    path("export-pdf/", views.export_pdf, name="export_pdf"),

    # Profile
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Attendance
    path("attendance/", views.attendance_list, name="attendance"),
    path("attendance/edit/<int:id>/", views.edit_attendance, name="edit_attendance"),
    path("attendance/delete/<int:id>/", views.delete_attendance, name="delete_attendance"),
    path("attendance/excel/", views.attendance_excel, name="attendance_excel"),
    path("attendance/pdf/", views.attendance_pdf, name="attendance_pdf"),

]