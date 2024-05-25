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
from patient.models import PatientPrimaryData,FT,PHR,Visit,JDD,Test,MedicalTestResult,PatientTest, TestForm,TestReport,Medicine
from patient.models import PatientPrescription, PrescribedMedicine

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



def consultantDoctor_patientDiagonise(request, appointment_id):
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
        
        test_reports = TestReport.objects.filter(patient_test__appointment_id=appointment_id)
        med=Medicine.objects.all()
        context = {
            'pd': pd,
            'ad': ad,
            'phr': phr,
            'rep': rep,
            'tests': tests,
            'test_reports': test_reports,
            'med':med,
        }
        print(ad,pd,pid,phr,tests,rep,test_reports)
        print("----")
        print(rep)
        print(test_reports)
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
    # if request.method == 'POST':
    #     print(request.POST)
    #     tablet_names = request.POST.getlist('tablet_name[]')
    #     feeding_rules = request.POST.getlist('feeding_rule[]')
    #     dosages = request.POST.getlist('dosage[]')
    #     feeding_days = request.POST.getlist('feeding_days[]')

    #     # Print the values
    #     for i in range(len(tablet_names)):
    #         print(f"Medicine {i+1}:")
    #         print(f"Tablet Name: {tablet_names[i]}")
    #         print(f"Feeding Rule: {feeding_rules[i]}")
    #         print(f"feeding_days: {feeding_days[i]}")
    #         print(f"Dosage: {dosages[i]}")
            
    #     medicine_details_list = [
    #         {
    #             'tablet_name': tablet_names[i],
    #             'feeding_rule': feeding_rules[i],
    #             'dosage': dosages[i],
    #             'feeding_days': feeding_days[i]
    #         }
    #         for i in range(len(tablet_names))
    #     ]
    #     return render(request,'prescription.html',{'medicine_details_list':medicine_details_list})
    if request.method == 'POST':
        # Process the submitted form data to extract the prescribed medicines
        print(request.POST)
        if request.method == 'POST':
            selected_medicines = []
            for key, value in request.POST.items():
                if key.startswith('tablet_name'):
                    tablet_name = value
                    dosage = request.POST.get('dosage[' + key.split('[')[1], '')
                    feeding_rule = request.POST.get('feeding_rule[' + key.split('[')[1], '')
                    feeding_days = request.POST.get('feeding_days[' + key.split('[')[1], '')
                    selected_medicines.append({'tablet_name': tablet_name, 'dosage': dosage, 'feeding_rule': feeding_rule, 'feeding_days': feeding_days})
        
        # Assuming you have a prescription template named 'prescription.html'
        context = {
            'selected_medicines': selected_medicines,
        }
        return render(request, 'prescription.html', context)
    med=Medicine.objects.all()
    context={
        'med':med,
    }
    return render(request,'medicine.html',context)




def prescribe_medicine(request, appointment_id):
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
        
        test_reports = TestReport.objects.filter(patient_test__appointment_id=appointment_id)
        med=Medicine.objects.all()
        context = {
            'pd': pd,
            'ad': ad,
            'phr': phr,
            'rep': rep,
            'tests': tests,
            'test_reports': test_reports,
            'med':med,
        }
        print(ad,pd,pid,phr,tests,rep,test_reports)
        print("----")
        print(rep)
        print(test_reports)
        if request.method == 'POST':
            prescription = PatientPrescription.objects.create(
                appointment_id=ad,
                patient_id=pd,
                chief_complaints=request.POST.get('chief_complaints'),
                clinical_findings=request.POST.get('clinical_findings'),
                investigations=request.POST.get('investigations'),
                diagnosis=request.POST.get('diagnosis'),
                procedures_conducted=request.POST.get('procedures_conducted'),
                advice_given=request.POST.get('advice_given'),
                next_visit=request.POST.get('next_visit')
            )
        
            prescribed_medicines = []
            for key, value in request.POST.items():
                if key.startswith('tablet_name'):
                    tablet_name = value
                    dosage = request.POST.get('dosage[' + key.split('[')[1], '')
                    feeding_rule = request.POST.get('feeding_rule[' + key.split('[')[1], '')
                    feeding_days = request.POST.get('feeding_days[' + key.split('[')[1], '')
                    prescribed_medicines.append(PrescribedMedicine(
                        prescription=prescription,
                        medicine=Medicine.objects.get(name=tablet_name),
                        dosage=dosage,
                        feeding_rule=feeding_rule,
                        feeding_time=request.POST.get('feeding_time[' + key.split('[')[1], ''),
                        feeding_days=feeding_days
                    ))
        
            PrescribedMedicine.objects.bulk_create(prescribed_medicines)
        
            # Assuming you have a prescription template named 'prescription.html'
            context = {
                'prescription': prescription,
                'prescribed_medicines': prescribed_medicines,
            }
            print(request.POST)
            return render(request, 'prescription.html', context)
    
        return render(request, 'consultant_doctor/consultantDoctor_prescribe_medicine.html', context)
    
    except Visit.DoesNotExist:
        return HttpResponse("Visit not found.")
    except PatientPrimaryData.DoesNotExist:
        return HttpResponse("Patient primary data not found.")
    except JDD.DoesNotExist:
        return HttpResponse("JDD data not found.")