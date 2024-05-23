from django.urls import path
from . import views

app_name = 'junior_doctor'

urlpatterns = [

    path('juniorDoctor_dashboard',views.juniorDoctor_dashboard,name='juniorDoctor_dashboard'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('page_not_found',views.page_not_found,name="page_not_found"),
    path('juniorDoctor_appointmentList',views.juniorDoctor_appointmentList,name="juniorDoctor_appointmentList"),
    path('juniorDoctor_patientList',views.juniorDoctor_patientList,name="juniorDoctor_patientList"),
    path('juniorDoctor_apl',views.juniorDoctor_apl,name="juniorDoctor_apl"),
    path('juniorDoctor_appointmentList_FilterbyDate',views.juniorDoctor_appointmentList_FilterbyDate,name="juniorDoctor_appointmentList_FilterbyDate"),
    path('juniorDoctor_patientDiagonise/<str:appointment_id>/',views.juniorDoctor_patientDiagonise,name="juniorDoctor_patientDiagonise"),
    # path('juniorDoctor_patientDiagonise_View_Edit/<str:patient_id>/',views.juniorDoctor_patientDiagonise_View_Edit,name="juniorDoctor_patientDiagonise_View_Edit"),
    path('juniorDoctor_patientView/<str:patient_id>/',views.juniorDoctor_patientView,name="juniorDoctor_patientView"),
    path('juniorDoctor_patientDiagonise_View_Edit/<str:appointment_id>/', views.juniorDoctor_patientDiagonise_View_Edit, name="juniorDoctor_patientDiagonise_View_Edit"),
    
]
