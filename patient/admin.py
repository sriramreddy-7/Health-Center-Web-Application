from django.contrib import admin
from patient.models import PatientPrimaryData,FT,RP,PHR,Visit,JDD,Test,MedicalTestResult
# Register your models here.
admin.site.register(PatientPrimaryData)
# admin.site.register(PatientCount)
# admin.site.register(Appointment)
admin.site.register(Visit)
admin.site.register(FT)
admin.site.register(RP)
admin.site.register(PHR)
admin.site.register(JDD)
admin.site.register(Test)
admin.site.register(MedicalTestResult)