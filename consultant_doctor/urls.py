from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'consultant_doctor'

urlpatterns = [
    path('consultantDoctor_dashboard',views.consultantDoctor_dashboard,name='consultantDoctor_dashboard'),
    path('logout_view',views.logout_view,name="logout_view"),
    path('consultantDoctor_patientList',views.consultantDoctor_patientList,name="consultantDoctor_patientList"),
    path('consultantDoctor_appointmentList',views.consultantDoctor_appointmentList,name="consultantDoctor_appointmentList"),
    path('consultantDoctor_patientDiagonise/<str:appointment_id>/',views.consultantDoctor_patientDiagonise,name="consultantDoctor_patientDiagonise"),
    path('consultantDoctor_patientDiagonise_View_Edit/<str:patient_id>/',views.consultantDoctor_patientDiagonise_View_Edit,name="consultantDoctor_patientDiagonise_View_Edit"),
    path('consultantDoctor_precribeTest/<str:appointment_id>/',views.consultantDoctor_precribeTest,name="consultantDoctor_precribeTest"),
    path('consultantDoctor_prescription',views.consultantDoctor_prescription,name='consultantDoctor_prescription'),
    path('consultantDoctor_patientView/<str:patient_id>/',views.consultantDoctor_patientView,name="consultantDoctor_patientView"),
    path('consultantDoctor_all_patients_medical_details',views.consultantDoctor_all_patients_medical_details,name='consultantDoctor_all_patients_medical_details'),
    path('medicine',views.medicine,name="medicine"),
    path('prescribe_medicine/<str:appointment_id>/',views.prescribe_medicine,name="prescribe_medicine"),
    path('view_prescription/<str:appointment_id>/',views.view_prescription,name="view_prescription"),
    path("all_patient_reports",views.all_patient_reports,name="all_patient_reports"),
    # path('prescription',views.prescription,name="prescription"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

