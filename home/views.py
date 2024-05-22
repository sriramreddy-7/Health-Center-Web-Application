from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,logout,login
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.cache import never_cache


def index(request):
    return render(request,'index.html')

def login_page(request):
    return render(request,'login.html')

def error_404(request):
    return render(request,'error-404.html')

def receptionist_login(request):
    context={
        "msg":"Receptionist",
    }
    if request.method=='POST':
        user=authenticate(
        username=request.POST['username'],
        password=request.POST['password']
        )
        if user is not None:
            login(request,user)
            # return render(request,'receptionist_dashboard.html')
            # return  HttpResponse('Sucessfully Logged in')
            return redirect('receptionist:receptionist_dashboard')
            # return render(request, 'ReceptionistDBPage.html')
        else:
            return render(request,'receptionist_login.html',context)

    else:
        return render(request,'receptionist_login.html',context)


def lab_incharge_login(request):
    context={
        "msg":" Lab Incharge ",
    }
    if request.method=='POST':
        user=authenticate(
        username=request.POST['username'],
        password=request.POST['password']
        )
        if user is not None:
            login(request,user)
            # return render(request,'receptionist_dashboard.html')
            # return  HttpResponse('Sucessfully Logged in')
            return redirect('lab_incharge:lab_incharge_dashboard')
            # return render(request, 'ReceptionistDBPage.html')
        else:
            return render(request,'lab_incharge_login.html',context)

    else:
        return render(request,'lab_incharge_login.html',context)

def junior_doctor_login(request):
    context={
        "msg":"Junior Doctor",
    }
    if request.method=='POST':
        user=authenticate(
        username=request.POST['username'],
        password=request.POST['password']
        )
        if user is not None:
            login(request,user)
            # return render(request,'receptionist_dashboard.html')
            # return  HttpResponse('Sucessfully Logged in')
            return redirect('junior_doctor:juniorDoctor_dashboard')
            # return render(request, 'ReceptionistDBPage.html')
        else:
             return render(request,'junior_doctor_login.html',context)

    else:
        return render(request,'junior_doctor_login.html',context)


def consultant_doctor_login(request):
    context={
        "msg":"Consultant Doctor",
    }
    if request.method=='POST':
        user=authenticate(
        username=request.POST['username'],
        password=request.POST['password']
        )
        if user is not None:
            login(request,user)
            # return render(request,'receptionist_dashboard.html')
            # return  HttpResponse('Sucessfully Logged in')
            return redirect('consultant_doctor:consultantDoctor_dashboard')
            # return render(request, 'ReceptionistDBPage.html')
        else:
            return render(request,'consultant_doctor_login.html',context)

    else:
        return render(request,'consultant_doctor_login.html',context)



def admin_login(request):
    context={
        "msg":"Hospital Admin",
    }
    if request.method=='POST':
        user=authenticate(
        username=request.POST['username'],
        password=request.POST['password']
        )
        if user is not None:
            login(request,user)
            # return render(request,'receptionist_dashboard.html')
            # return  HttpResponse('Sucessfully Logged in')
            return redirect('hospital_admin:admin_dashboard')
            # return render(request, 'ReceptionistDBPage.html')
        else:
            return render(request,'admin_login.html',context)

    else:
        return render(request,'admin_login.html',context)

