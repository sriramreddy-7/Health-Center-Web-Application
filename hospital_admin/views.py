from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,logout,login
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from hospital_admin.models import Employee

def admin_dashboard(request):
    # emp=Employee.objects.get(username=request.user)
    # context= {
    #     'emp':emp
    # }
    user=User.objects.get(username=request.user)
    context={
        'user':user
    }
    return render(request,'admin_dashboard.html',context)

@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('sessionid')
    return response

def login_logs(request):
    user_logs = LogEntry.objects.filter(user__isnull=False).order_by('-action_time')[:10]
    return render(request, 'admin_login_logs.html', {'user_logs': user_logs})

def staff_registration(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Debugging line to print POST data
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        emp_phone = request.POST.get('phone_number')
        emp_dob = request.POST.get('date_of_birth')
        emp_gender = request.POST.get('gender')
        emp_type = request.POST.get('emp_type')
        emp_profile_picture = request.FILES.get('emp_profile_picture')

        EMP_TYPE_CHOICES = {
            'Receptionist': 'RP',
            'Laboratory_Technician': 'LT',
            'Junior_Doctor': 'JD',
            'Consultant_Doctor': 'CD',
        }

        # Validate input
        if not (password and email and first_name and last_name and emp_phone and emp_dob and emp_gender and emp_type):
            messages.error(request, 'Please fill out all fields.')
            return redirect('hospital_admin:staff_registration')

        try:
            with transaction.atomic():
                # Create the User first to get the instance for Employee
                user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name, password=password)
                print("User created:", user)  # Debugging line to check user creation

                # Generate the emp_id
                prefix = 'CCHC'
                emp_type_code = EMP_TYPE_CHOICES.get(emp_type, 'XX')
                count = Employee.objects.filter(emp_type=emp_type).count() + 1
                emp_id = f"{prefix}{emp_type_code}{count:03d}"
                print("Generated emp_id:", emp_id)  # Debugging line to check emp_id generation

                # Create Employee with the generated emp_id
                emp = Employee(
                    user=user,
                    emp_id=emp_id,
                    emp_phone=emp_phone,
                    emp_dob=emp_dob,
                    emp_gender=emp_gender,
                    emp_type=emp_type,
                    emp_profile_picture=emp_profile_picture
                )
                emp.save()
                print("Employee created:", emp)  # Debugging line to check employee creation

                # Update the user with the emp_id as username
                user.username = emp_id
                user.save()
                print("Updated user username to emp_id:", user.username)  # Debugging line to check username update

            messages.success(request, 'Staff Registered Successfully')
            return redirect('hospital_admin:employee_list')
        except IntegrityError as e:
            # Clean up the user if created
            print("IntegrityError occurred:", e)  # Debugging line to check for integrity errors
            user.delete()
            messages.error(request, f'An error occurred: {e}')
            return redirect('hospital_admin:staff_registration')
        except Exception as e:
            print("Unexpected error occurred:", e)  # Debugging line to check for unexpected errors
            messages.error(request, f'Unexpected error: {e}')
            return redirect('hospital_admin:staff_registration')
    return render(request, 'admin/staff_registration.html')



def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'admin/employee_list.html', {'employees': employees})