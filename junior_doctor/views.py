from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,logout,login
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from patient.models import PatientPrimaryData,FT,PHR,Visit,JDD
# Create your views here.
from datetime import datetime

def juniorDoctor_dashboard(request):
    patient=Visit.objects.all()[:6]
    context={
        'patient':patient,
    }
    return render(request,'juniorDoctor_dashboard.html',context)

def juniorDoctor_appointmentList(request):
    appointments=Visit.objects.all()
    for appointment in appointments:
        try:
            jdd_data=JDD.objects.get(appointment_id=appointment)
            appointment.jdd_data_present =True
        except JDD.DoesNotExist:
            appointment.jdd_data_present = False
    return render(request,'juniorDoctor_appointmentList.html',{'appointments':appointments})

def page_not_found(request):
    return render(request,'page_not_found.html')

def juniorDoctor_patientList(request):
    patient=PatientPrimaryData.objects.all()
    patient_count=PatientPrimaryData.objects.count()
    return render(request,'juniorDoctor_patientList.html',{'patient':patient,'patient_count':patient_count})


def juniorDoctor_appointmentList_FilterbyDate(request):
    patient=Visit.objects.all()
    now= datetime.now()
    return render(request,'juniorDoctor_appointmentList_FilterbyDate.html',{'patient':patient,'now':now })

@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('sessionid')
    return response

# def juniorDoctor_patientDiagonise(request,appointment_id):
#     if request.method == 'POST':
#         height = request.POST['height']
#         weight = request.POST['weight']
#         pulse = request.POST['pulse']
#         bp = request.POST['bp']
#         blood_group=request.POST['blood_group']
#         is_diabetic = 'is_diabetic' in request.POST
#         diabetic_level = request.POST['diabetic_level'] if is_diabetic else None
#         phi = request.POST['phi']
#         pov = request.POST['pov']
#         remarks = request.POST['remarks']
#         appointment_id=request.POST['appointment_id']
#         visit = Visit.objects.get(appointment_id=appointment_id)
#         patient_id = PatientPrimaryData.objects.get(id=visit.patient_id_id)
#         print(appointment_id) 
#         print(patient_id)
#         print(height)
#         print(weight)
#         print(pulse)
#         print(bp)
#         print(blood_group)
#         print(is_diabetic)
#         print(phi)
#         print(pov)
#         print(remarks)
#         health_record = JDD.objects.create(
#             appointment_id=appointment_id,
#             patient_id = patient_id,
#             height=height,
#             weight=weight,
#             pulse=pulse,
#             bp=bp,
#             blood_group=blood_group,
#             is_diabetic=is_diabetic,
#             diabetic_level=diabetic_level,
#             phi=phi,
#             pov=pov,
#             remarks=remarks
#         )
#         health_record.save()
#         return redirect('junior_doctor:juniorDoctor_appointmentList')
#     ad=Visit.objects.get(appointment_id=appointment_id)
#     pid=ad.patient_id
#     pd=PatientPrimaryData.objects.get(patient_id=pid)
#     context={
#         'pd':pd,
#         'ad':ad
#     }
#     return render(request,'juniorDoctor_patientDiagonise.html',context)

def juniorDoctor_patientDiagonise(request,appointment_id):
    if request.method == 'POST':
    # Retrieve data from the POST request
        height = request.POST['height']
        weight = request.POST['weight']
        pulse = request.POST['pulse']
        bp = request.POST['bp']
        blood_group = request.POST['blood_group']
        is_diabetic = request.POST.get('is_diabetic')
        if is_diabetic == 'False':
            diabetic_level =False
        else:
            diabetic_level = request.POST.get('diabetic_level') 
        phi = request.POST['phi']
        pov = request.POST['pov']
        remarks = request.POST['remarks']
        appointment_id = request.POST['appointment_id']
        # Get the visit and patient objects
        # print(appointment_id)
        # print(patient_id)
        print('Height:', height)
        print('Weight',weight)
        print('pulse:',pulse)
        print('bp',bp)
        print('blood_group',blood_group)
        print('is_diabetic',is_diabetic)
        print('PHI',phi)
        print('POV',pov)
        print('Remarks',remarks) 
        visit = Visit.objects.get(appointment_id=appointment_id)
        patient_id = PatientPrimaryData.objects.get(id=visit.patient_id_id)
        # Print the retrieved data for debugging purposes
        
        # Create a new JDD object
        health_record = JDD.objects.create(
            appointment_id=visit,
            patient_id=patient_id,
            height=height,
            weight=weight,
            pulse=pulse,
            bp=bp,
            blood_group=blood_group,
            is_diabetic=is_diabetic,
            diabetic_level=diabetic_level,
            phi=phi,
            pov=pov,
            remarks=remarks
        )
        # Save the JDD object
        health_record.save()
        # Redirect to the desired page
        return redirect('junior_doctor:juniorDoctor_appointmentList')

# Code for GET request or when the form is not submitted
    ad = Visit.objects.get(appointment_id=appointment_id)
    pid = ad.patient_id
    pd = PatientPrimaryData.objects.get(patient_id=pid)
    context = {
        'pd': pd,
        'ad': ad    
    }
    return render(request, 'juniorDoctor_patientDiagonise.html', context)



def juniorDoctor_patientDiagonise_View_Edit(request,patient_id):
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    # ad=ValueError.objects.get(patient_id=patient_id)
    # md=PHR.objects.get(patient=pd)
    context={
        'pd':pd,
        # 'ad':ad,
        # 'md':md,
    }
    return render(request,'juniorDoctor_patientDiagonise_View_Edit.html',context)
    # else:
    #     return render(request,'page_not_found.html')
    # return render(request,'juniorDoctor_patientDiagonise_View_Edit.html',context)


def juniorDoctor_apl(request):
    jdoctor=JDD.objects.all()
    context={
        'jdoctor':jdoctor,
    }
    for i in jdoctor:
        print(i)
    return render(request,'juniorDoctor_apl.html',context)


def juniorDoctor_patientView(request,patient_id):
    
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    app_id=JDD.objects.filter(patient_id=pd)
    context={
        'pd':pd,
        'app_id':app_id,
    }
    return render(request,'juniorDoctor_patientView.html',context)