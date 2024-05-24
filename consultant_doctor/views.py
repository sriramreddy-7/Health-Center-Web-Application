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
from patient.models import PatientPrimaryData,FT,PHR,Visit,JDD,Test,MedicalTestResult


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
        
        try:
            rep = MedicalTestResult.objects.get(appointment_id=appointment_id)
        except MedicalTestResult.DoesNotExist:
            rep = None

        context = {
            'pd': pd,
            'ad': ad,
            'phr': phr,
            'rep': rep,
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


def consultantDoctor_precribeTest(request,appointment_id):
    if request.method == 'POST':
        appointment_id=request.POST.get('appointment_id')
        patient_id=request.POST.get('patient_id')
        x_ray = request.POST.get('x_ray')
        echocardiogram = request.POST.get('echocardiogram')
        electrocardiogram=request.POST.get('electrocardiogram')
        mri = request.POST.get('mri')
        stress_test=request.POST.get('stress_test')
        est=request.POST.get('est')
        blood_test=request.POST.get('blood_test')
        urine_test=request.POST.get('urine_test')
        ct_scan=request.POST.get('ct_scan')
        thread_mill_test = request.POST.get('thread_mill_test')
        echo=request.POST.get('echo')
        angiography=request.POST.get('angiography')
        print('Appointment_Id',appointment_id)
        print('Patient_Id',patient_id)
        print('X_Ray',x_ray)
        print('echocardiogram',echocardiogram)
        print('electrocardiogram',electrocardiogram)
        print('MRI Scan', mri)
        print('stress_test',stress_test)
        print('Blood Test',blood_test)
        print('Urine Test',urine_test)
        print('est',est)
        print('ct_scan',ct_scan)
        print('ECG',est)
        print('echo',echo)
        print('angiography',angiography)
        print('thread_mill_test ',thread_mill_test )
        visit = Visit.objects.get(appointment_id=appointment_id)
        patient_id = PatientPrimaryData.objects.get(id=visit.patient_id_id)
        test=Test.objects.create(
            appointment_id=visit,
            patient_id=patient_id,
            test1=x_ray,
            test2=echocardiogram,
            test3=electrocardiogram,
            test4=mri,
            test5=stress_test,
            test6=est,
            test7=blood_test,
            test8=urine_test,
            test9=ct_scan,
            test10=thread_mill_test,
            test11=echo,
            test12=angiography, 
        )
        test.save()
        # return HttpResponse('<h1 style="color:green;">The Test Precribtion is Submitted to the Lab Incharge </h1>')
        return redirect('consultant_doctor:consultantDoctor_appointmentList')
    ad=Visit.objects.get(appointment_id=appointment_id)
    pid=ad.patient_id
    pd=PatientPrimaryData.objects.get(patient_id=pid)
    context={
        'ad':ad,
        'pd':pd,
    }
    return render(request,'consultantDoctor_precribeTest.html',context)


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