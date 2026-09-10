"""
URL configuration for ftsproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from mainapp import views

# adminapp ka views import kiya
from adminapp.views import *
# empapp ka views
from empapp.views import *

# for media files save
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # mainapp url
    path('', views.home, name='home'),
    path('contact/',views.contact,name='contact'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('userlogin/',views.userlogin,name='userlogin'),
    # adminapp urls
    path('adminlogout/',adminlogout,name="adminlogout"), # admin logout
    path('admindash/', admindash, name='admindash'),
    path('adminpass/',adminpass,name="adminpass"), # admin password change
    path('adddept/', adddept, name="adddept"), # Add Department url
    path('viewdept/', viewdept, name="viewdept"), # view department url
    path('addemp/', addemp, name="addemp"), # add Employees
    path('viewemp/', viewemp, name="viewemp"), # View Employee
    path('deldept/<did>',deldept,name='deldept'), # delete department
    path('allfiles/', allfiles, name="allfiles"), # all files access admin

    # empapp ka urls
    path('empdash/',empdash,name='empdash'),
    path('emplogout/',emplogout,name='emplogout'),
    path('viewprofile/',viewprofile,name='viewprofile'),
    path('updateprofile/',updateprofile,name='updateprofile'),
    path('initiatefile/',initiatefile,name='initiatefile'),
    path('viewfiles/',viewfiles,name='viewfiles'),

    path('empchangepass/',empchangepass,name='empchangepass'),
    path('recivedfiles/',recivedfiles,name='recivedfiles'),
    path('filedetails/<fid>',filedetails,name='filedetails'),
    path('closefile/<fid>',closefile,name='closefile'),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
