from django.shortcuts import render, redirect
from .models import LoginInfo
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')


def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            emp = LoginInfo.objects.get(username=username, usertype="employee")
            if check_password(password, emp.password) or emp.password == password:
                if emp.password == password:
                    emp.password = make_password(password)
                    emp.save()
                messages.success(request, 'Welcome Employee')
                request.session['eid'] = emp.username
                return redirect('empdash')
            else:
                messages.warning(request, "Invalid username or password")
                return redirect('userlogin')
        except LoginInfo.DoesNotExist:
            messages.warning(request, "Invalid username or password")
            return redirect('userlogin')
    return render(request, "userlogin.html")

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            admin = LoginInfo.objects.get(username=username, usertype="admin")
            if check_password(password, admin.password) or admin.password == password:
                if admin.password == password:
                    admin.password = make_password(password)
                    admin.save()
                messages.success(request, 'Welcome Admin')
                request.session['adminid'] = admin.username
                return redirect('admindash')
            else:
                messages.warning(request, 'Invalid username or password')
                return redirect('adminlogin')
        except LoginInfo.DoesNotExist:
            messages.warning(request, 'Invalid username or password')
            return redirect('adminlogin')
    return render(request, "adminlogin.html")

