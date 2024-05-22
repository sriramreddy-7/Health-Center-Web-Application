"""cchc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from home import views
from django.conf.urls.static import static


urlpatterns = [
    path('receptionist/', include('receptionist.urls', namespace='receptionist')),
    path('junior_doctor/', include('junior_doctor.urls', namespace='junior_doctor')),
    path('consultant_doctor/', include('consultant_doctor.urls', namespace='consultant_doctor')),
    path('lab_incharge/', include('lab_incharge.urls', namespace='lab_incharge')),
    path('hospital_admin/', include('hospital_admin.urls', namespace='hospital_admin')),

    path('',views.index,name="index"),
    path('login',views.login_page,name="login"),
    path('receptionist_login',views.receptionist_login,name="receptionist_login"),
    path('junior_doctor_login',views.junior_doctor_login,name="junior_doctor_login"),
    path('lab_incharge_login',views.lab_incharge_login,name="lab_incharge_login"),
    path('consultant_doctor_login',views.consultant_doctor_login,name="consultant_doctor_login"),
    path('admin_login',views.admin_login,name="admin_login"),
    path('error-404',views.error_404,name="error-404"),
    # path('',include('home.urls',namespace='home')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
