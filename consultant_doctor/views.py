from django.shortcuts import render,get_object_or_404

from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,logout,login
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from patient.models import PatientPrimaryData,FT,PHR,Visit,JDD,Test,MedicalTestResult,PatientTest, TestForm


def consultantDoctor_dashboard(request):
    today= timezone.now().date()
    patient_count=PatientPrimaryData.objects.count()
    appt_count=Visit.objects.filter(visit_date=today).count()
    common_records = PatientPrimaryData.objects.filter(patient_id__in=FT.objects.values('patient_id'))
    data={
        'patient_count':patient_count,
        'appt_count':appt_count,
        'common_records':common_records,
    }
    return render(request,'consultantDoctor_dashboard.html',data)

@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('sessionid')
    return response

def consultantDoctor_patientList(request):
    patient=PatientPrimaryData.objects.all()
    return render(request,'consultantDoctor_patientList.html',{'patient':patient})

def consultantDoctor_appointmentList(request):
    patient=Visit.objects.all()
    return render(request,'consultantDoctor_appointmentList.html',{'patient':patient})


def consultantDoctor_patientDiagonise(request,appointment_id):
    try:
        
        ad = get_object_or_404(Visit, appointment_id=appointment_id)
        pid = ad.patient_id
        pd = get_object_or_404(PatientPrimaryData, patient_id=pid)
        phr = get_object_or_404(JDD, appointment_id=appointment_id)
        tests = TestForm.objects.all()
        try:
            rep = MedicalTestResult.objects.get(appointment_id=appointment_id)
        except MedicalTestResult.DoesNotExist:
            rep = None

        context = {
            'pd': pd,
            'ad': ad,
            'phr': phr,
            'rep': rep,
            'tests':tests, 
        }
        return render(request, 'consultantDoctor_patientDiagonise.html', context)
    except Visit.DoesNotExist:
        return HttpResponse("Visit not found.")
    except PatientPrimaryData.DoesNotExist:
        return HttpResponse("Patient primary data not found.")
    except JDD.DoesNotExist:
        return HttpResponse("JDD data not found.")
        # return HttpResponse('<h1 style="color:red;">Oops! This Patient is not yet compeleted the Initial Diagonisis At Junior Doctor</h1>')


def consultantDoctor_patientDiagonise_View_Edit(request,patient_id):
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    # ad=FT.objects.get(patient_id=patient_id)
    # md=PHR.objects.get(patient=pd)
    context={
        'pd':pd,
        # 'ad':ad,
        # 'md':md,
    }
    return render(request,'consultantDoctor_patientDiagonise_View_Edit.html',context)


def consultantDoctor_precribeTest(request, appointment_id):
    if request.method == 'POST':
        appointment = Visit.objects.get(appointment_id=appointment_id)
        patient = PatientPrimaryData.objects.get(id=appointment.patient_id_id)

        selected_tests = request.POST.getlist('test_ids')

        patient_test = PatientTest.objects.create(
            appointment_id=appointment,
            patient_id=patient,
        )

        for test_id in selected_tests:
            test = TestForm.objects.get(id=test_id)
            patient_test.tests.add(test)

        patient_test.save()

        return redirect('consultant_doctor:consultantDoctor_appointmentList')

    ad = Visit.objects.get(appointment_id=appointment_id)
    pd = PatientPrimaryData.objects.get(patient_id=ad.patient_id)
    tests = TestForm.objects.all()
    context = {
        'ad': ad,
        'pd': pd,
        'tests': tests,
    }
    return render(request, 'consultantDoctor_precribeTest.html', context)


def consultantDoctor_prescription(request):
    return render(request,'consultantDoctor_prescription.html')



def consultantDoctor_patientView(request,patient_id):
    # patient_id='CCHC202307050008'
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    app_id=JDD.objects.filter(patient_id=pd)
    context={
        'pd':pd,
        'app_id':app_id,
    }
    return render(request,'consultantDoctor_patientView.html',context)



def consultantDoctor_all_patients_medical_details(request):
    pd=PatientPrimaryData.objects.all()
    app_id=JDD.objects.all()
    context={
        'pd':pd,
        'app_id':app_id,
    }
    return render(request,'consultantDoctor_all_patients_medical_details.html',context)


def medicine(request):
    if request.method == 'POST':
        tablet_names = request.POST.getlist('tablet_name[]')
        feeding_rules = request.POST.getlist('feeding_rule[]')
        dosages = request.POST.getlist('dosage[]')
        feeding_days = request.POST.getlist('feeding_days[]')

        # Print the values
        for i in range(len(tablet_names)):
            print(f"Medicine {i+1}:")
            print(f"Tablet Name: {tablet_names[i]}")
            print(f"Feeding Rule: {feeding_rules[i]}")
            print(f"feeding_days: {feeding_days[i]}")
            print(f"Dosage: {dosages[i]}")
            
        medicine_details_list = [
            {
                'tablet_name': tablet_names[i],
                'feeding_rule': feeding_rules[i],
                'dosage': dosages[i],
                'feeding_days': feeding_days[i]
            }
            for i in range(len(tablet_names))
        ]
        return render(request,'prescription.html',{'medicine_details_list':medicine_details_list})

        
    return render(request,'medicine.html')