from django.urls import path
from . import views

app_name = 'lab_incharge'

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('trail/<str:appointment_id>/',views.trail,name="trail"),
    path('lab_incharge_dashboard',views.lab_incharge_dashboard,name='lab_incharge_dashboard'),
    path('logout_view',views.logout_view,name="logout_view"),
    path('lab_incharge_patient_wise_report',views.lab_incharge_patient_wise_report,name="lab_incharge_patient_wise_report"),
    path('lab_incharge_upload_report/<str:appointment_id>/',views.lab_incharge_upload_report,name="lab_incharge_upload_report"),
    path('lab_Incharge_patient_reports',views.lab_Incharge_patient_reports,name="lab_Incharge_patient_reports"),
    path('lab_Incharge_patient_reports_gallery',views.lab_Incharge_patient_reports_gallery,name="lab_Incharge_patient_reports_gallery"),
    path('lab_incharge_test_orders',views.lab_incharge_test_orders,name="lab_incharge_test_orders"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)