"""heart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from admins import views as admins
from django.urls import path
from users import views as usr
from . import views as mainView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', mainView.index, name='index'),
    path("UserRegister/", mainView.UserRegister, name="UserRegister"),
    path("AdminLogin/", mainView.AdminLogin, name="AdminLogin"),
    path('index/', mainView.index, name='index'),
    path("UserLogin/", mainView.UserLogin, name="UserLogin"),

    ### User Side Views
    path("UserRegisterActions/", usr.UserRegisterActions, name="UserRegisterActions"),
    path("UserLoginCheck/", usr.UserLoginCheck, name="UserLoginCheck"),
    path("UserHome/", usr.UserHome, name="UserHome"),
    path("UserMachineLearning/", usr.UserMachineLearning, name="UserMachineLearning"),
    path("upload_xray_form/", usr.upload_xray_form, name="upload_xray_form"),
    path("UserXRayImageActions/", usr.UserXRayImageActions, name="UserXRayImageActions"),
    path("UserCropped/", usr.UserCropped, name="UserCropped"),


    ### Admin Side Views
    path("AdminLoginCheck/", admins.AdminLoginCheck, name="AdminLoginCheck"),
    path("AdminHome/", admins.AdminHome, name="AdminHome"),
    path("ViewRegisteredUsers/", admins.ViewRegisteredUsers, name="ViewRegisteredUsers"),
    path("AdminActivaUsers/", admins.AdminActivaUsers, name="AdminActivaUsers"),
    # path("AdminDataPreProcess/", admins.AdminDataPreProcess, name="AdminDataPreProcess"),
    path("AdminViewResults/", admins.AdminViewResults, name="AdminViewResults"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

