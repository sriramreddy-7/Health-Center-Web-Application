from django.urls import path
from . import views

app_name = 'hospital_admin'

urlpatterns = [

    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('logout_view',views.logout_view,name="logout_view"),
    path('login_logs',views.login_logs,name="login_logs"),
    path('staff_registration',views.staff_registration,name='staff_registration'),
    path("employee_list",views.employee_list,name="employee_list"),
    path('patient_appointments',views.patient_appointments,name="patient_appointments"),
    path("appointment/<str:ap_id>/",views.appointment,name="appointment")

]