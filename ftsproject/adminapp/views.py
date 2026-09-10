from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import *
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    total_files = File.objects.all().count()
    total_emp = Employee.objects.all().count()
    total_dep = Department.objects.all().count()
    pending_files = File.objects.filter(status="OPEN").count()
    context = {
        'adminid': adminid,
        'total_files': total_files,
        'total_emp': total_emp,
        'total_dep': total_dep,
        'pending_files': pending_files,
    }
    return render(request, 'admindash.html', context)

# admin logout views 
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, 'Admin Logged Out Successfully')
        return redirect('adminlogin')
    else:
        return redirect('adminlogin')

# add Department
def adddept(request):
    if 'adminid' not in request.session:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid': adminid,
    }
    if request.method == 'POST':
        dept_name = request.POST.get('dept_name')
        if Department.objects.filter(dept_name=dept_name).exists():
            messages.warning(request, "This Department already exists")
            return redirect('adddept')
        dep = Department.objects.create(dept_name=dept_name)
        messages.success(request, 'Department Added Successfully')
        return redirect('viewdept')
    return render(request, 'adddept.html', context)

# Views Department
def viewdept(request):
    if 'adminid' not in request.session:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    depts = Department.objects.all()
    context = {
        'adminid': adminid,
        'depts': depts,
    }
    return render(request, 'viewdept.html', context)

# Add Employees
def addemp(request):
    if 'adminid' not in request.session:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    depts = Department.objects.all()
    context = {
        'adminid': adminid,
        'depts': depts,
    }
    if request.method == 'POST':
        empid = request.POST.get('empid')
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        email = request.POST.get('email')
        designation = request.POST.get('designation')
        dept_id = request.POST.get('dept_id')

        dept = Department.objects.get(id=dept_id)
        if LoginInfo.objects.filter(username=email).exists():
            messages.warning(request, 'This email already added')
            return redirect('addemp')

        hashed_password = make_password('12345678')
        log = LoginInfo.objects.create(usertype='employee', username=email, password=hashed_password)
        emp = Employee.objects.create(log=log, empid=empid, name=name, contactno=contactno, email=email, designation=designation, department=dept)
        messages.success(request, 'Employee added successfully')
        return redirect('viewemp')
    return render(request, 'addemp.html', context)

# View Employees
def viewemp(request):
    if 'adminid' not in request.session:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    emps = Employee.objects.all()
    context = {
        'adminid': adminid,
        'emps': emps,
    }
    return render(request, 'viewemp.html', context)

# Admin password changing 
def adminpass(request):
    if 'adminid' not in request.session:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    admin = LoginInfo.objects.get(username=adminid)
    context = {
        'adminid': adminid,
    }
    if request.method == "POST":
        password = request.POST.get('password')
        npassword = request.POST.get('npassword')
        cpassword = request.POST.get('cpassword')
        if npassword != cpassword:
            messages.warning(request, "New password not match confirm password")
            return redirect('adminpass')
        if check_password(password, admin.password) or admin.password == password:
            admin.password = make_password(npassword)
            admin.save()
            messages.success(request, 'Password changed successfully')
            return redirect('adminlogin')
        else:
            messages.warning(request, 'Current password is incorrect')
            return redirect('adminpass')
    return render(request, 'adminpass.html', context)

# Delete department
def deldept(request, did):
    if 'adminid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('adminlogin')
    
    if Department.objects.filter(id=did).exists():
        try:
            Department.objects.get(id=did).delete()
            messages.success(request, "Department deleted successfully")
        except Exception as e:
            messages.error(request, "Cannot delete department: Employees are still assigned to it.")
        return redirect('viewdept')
    else:
        return redirect('viewdept')

# all files access code
def allfiles(request):
    if 'adminid' not in request.session:
        messages.error(request, 'Please Login First')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    files = File.objects.all()
    context = {
        'adminid': adminid,
        'files': files,
    }
    return render(request, 'allfiles.html', context)