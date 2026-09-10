from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import *
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def empdash(request):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    total_files = File.objects.filter(initiated_by=emp).count()
    pending_files = File.objects.filter(current_holder=emp, status="OPEN").count()
    close_files = File.objects.filter(initiated_by=emp, status="CLOSED").count()
    context = {
        'eid': eid,
        'emp': emp,
        'total_files': total_files,
        'pending_files': pending_files,
        'close_files': close_files,
    }
    return render(request, 'empdash.html', context)

# admin logout views 
def emplogout(request):
    if 'eid' in request.session:
        del request.session['eid']
        messages.success(request, 'Employee Logged Out Successfully')
        return redirect('userlogin')
    else:
        return redirect('userlogin')

# view profiles
def viewprofile(request):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    context = {
        'eid': eid,
        'emp': emp,
    }
    return render(request, 'viewprofile.html', context)

# update profile
def updateprofile(request):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    context = {
        'eid': eid,
        'emp': emp,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        picture = request.FILES.get('picture')
        address = request.POST.get('address')

        emp.name = name
        emp.contactno = contactno
        if picture:
            emp.picture = picture
        emp.address = address
        emp.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('viewprofile')
    return render(request, 'updateprofile.html', context)

# change password views
def empchangepass(request):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp_user = LoginInfo.objects.get(username=eid)
    context = {
        'eid': eid,
        'emp': emp_user,
    }
    if request.method == "POST":
        password = request.POST.get('password')
        npassword = request.POST.get('npassword')
        cpassword = request.POST.get('cpassword')
        if npassword != cpassword:
            messages.warning(request, "New password does not match confirm password")
            return redirect('empchangepass')
        if check_password(password, emp_user.password) or emp_user.password == password:
            emp_user.password = make_password(npassword)
            emp_user.save()
            messages.success(request, 'Password changed successfully')
            return redirect('emplogout')
        else:
            messages.warning(request, 'Current password is incorrect')
            return redirect('empchangepass')
    return render(request, 'empchangepass.html', context)

# initiatefile 
def initiatefile(request):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')

    emp = Employee.objects.get(email=eid)
    employees = Employee.objects.exclude(id=emp.id)  # Prevent self-forwarding
    context = {
        'eid': eid,
        'emp': emp,
        'employees': employees,
    }
    if request.method == "POST":
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        file_attachment = request.FILES.get('file_attachment')
        emp_id = request.POST.get('emp_id')
        forwarded_to = Employee.objects.get(email=emp_id)

        fi = File.objects.create(
            title=title,
            subject=subject,
            file_attachment=file_attachment,
            initiated_by=emp,
            current_holder=forwarded_to,
        )

        FileMovement.objects.create(
            file=fi,
            from_employee=emp,
            to_employee=forwarded_to,
            action="CREATE",
            remarks="File created successfully",
        )
        messages.success(request, "File initiated successfully")
        return redirect('viewfiles')
    return render(request, 'initiatefile.html', context)

# view files
def viewfiles(request):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    files = File.objects.filter(initiated_by=emp)

    context = {
        'eid': eid,
        'emp': emp,
        'files': files,
    }
    return render(request, 'viewfiles.html', context)

# Received files
def recivedfiles(request):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    files = File.objects.filter(Q(current_holder=emp) & Q(status="OPEN"))
    context = {
        'eid': eid,
        'emp': emp,
        'files': files,
    }
    return render(request, 'recivedfiles.html', context)

# Track file history views
def filedetails(request, fid):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    file = File.objects.get(file_no=fid)

    # 🔒 Authorization Check
    has_permission = (
        file.current_holder == emp or 
        file.initiated_by == emp or 
        FileMovement.objects.filter(file=file, from_employee=emp).exists() or 
        FileMovement.objects.filter(file=file, to_employee=emp).exists()
    )

    if not has_permission:
        messages.error(request, "Aapko is file ko dekhne ki permission nahi hai!")
        return redirect('recivedfiles')

    employees = Employee.objects.exclude(id=emp.id)  # Prevent forwarding to self
    file_moments = FileMovement.objects.filter(file=file)
    context = {
        'eid': eid,
        'emp': emp,
        'file': file,
        'employees': employees,
        'file_moments': file_moments,
    }
    if request.method == 'POST':
        if file.status != "OPEN":
            messages.error(request, "Closed file ko forward/close nahi kiya ja sakta.")
            return redirect('recivedfiles')

        emp_email = request.POST.get('emp_email')
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        to_employee = None
        if emp_email and action != "CLOSE":
            to_employee = Employee.objects.get(email=emp_email)

        if action == "CLOSE":
            file.status = "CLOSED"
            file.closed_at = timezone.now()
            file.save()
            FileMovement.objects.create(
                file=file,
                from_employee=emp,
                to_employee=None,
                action="CLOSE",
                remarks=remarks or "File closed",
            )
            messages.success(request, "File closed successfully")
            return redirect('recivedfiles')

        FileMovement.objects.create(
            file=file,
            from_employee=emp,
            to_employee=to_employee,
            action=action,
            remarks=remarks,
        )
        if to_employee:
            file.current_holder = to_employee
            file.save()
            messages.success(request, f"File {action} to {to_employee.name}")
        return redirect('recivedfiles')
    return render(request, 'filedetails.html', context)

# file closing views
def closefile(request, fid):
    if 'eid' not in request.session:
        messages.error(request, 'Please Login first')
        return redirect('userlogin')
    eid = request.session.get('eid')
    emp = Employee.objects.get(email=eid)
    file = File.objects.get(file_no=fid)

    # 🔒 Authorization check
    if file.current_holder != emp and file.initiated_by != emp:
        messages.error(request, "Aapko is file ko close karne ki permission nahi hai!")
        return redirect('recivedfiles')

    if file.status != "CLOSED":
        file.status = "CLOSED"
        file.closed_at = timezone.now()
        file.save()

        # Audit movement log
        FileMovement.objects.create(
            file=file,
            from_employee=emp,
            to_employee=None,
            action="CLOSE",
            remarks=f"File successfully closed by {emp.name}",
        )
        messages.success(request, "File closed successfully")
    else:
        messages.warning(request, "File is already closed.")
    return redirect('recivedfiles')