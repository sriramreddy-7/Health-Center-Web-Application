from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'hospital_admin'

urlpatterns = [

    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('logout_view',views.logout_view,name="logout_view"),
    path('login_logs',views.login_logs,name="login_logs"),
    path('staff_registration',views.staff_registration,name='staff_registration'),
    path("employee_list",views.employee_list,name="employee_list"),
    path('employee_profiles',views.employee_profiles,name="employee_profiles"),
    path('patient_appointments',views.patient_appointments,name="patient_appointments"),
    path("appointment/<str:ap_id>/",views.appointment,name="appointment"),
    path("admin_medical_test",views.admin_medical_test,name="admin_medical_test"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)