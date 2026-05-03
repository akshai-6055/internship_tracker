from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm # Used as base class in forms.py but we import CustomAuthenticationForm from forms
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse

from .forms import CustomUserCreationForm, InternshipForm, ApplicationForm, CustomAuthenticationForm
from .models import Internship, Application


# 🔹 Landing Page
def landing_page(request):
    featured_internships = Internship.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/landing.html', {'featured_internships': featured_internships})


# 🔹 Signup
def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            login(request, user)

            if user.is_admin:
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/signup.html', {'form': form})


# 🔹 Login (WITH ROLE SUPPORT 🔥)
def user_login(request):
    user_type = request.GET.get('type')  # admin / student

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # 🔒 Role validation
            if user_type == 'admin' and not user.is_admin:
                messages.error(request, "You are not an admin!")
                return redirect(f"{reverse('login')}?type=admin")

            if user_type == 'student' and not user.is_student:
                messages.error(request, "You are not a student!")
                return redirect(f"{reverse('login')}?type=student")

            login(request, user)
            messages.success(request, "Logged in successfully!")

            if user.is_admin:
                return redirect('admin_dashboard')
            return redirect('student_dashboard')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'core/login.html', {
        'form': form,
        'user_type': user_type
    })


# 🔹 Logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('landing_page')


# 🔹 Delete Account
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Account deleted successfully!")
        return redirect('landing_page')

    return render(request, 'core/delete_account.html')


# 🔹 Role Decorators
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


# ================= ADMIN ================= #

@admin_required
def admin_dashboard(request):
    internships = Internship.objects.all()
    applications = Application.objects.select_related('user', 'internship').all()

    return render(request, 'core/admin_dashboard.html', {
        'internships': internships,
        'applications': applications
    })


@admin_required
def create_internship(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Internship created successfully!")
            return redirect('admin_dashboard')
    else:
        form = InternshipForm()

    return render(request, 'core/internship_form.html', {
        'form': form,
        'title': 'Create Internship'
    })


@admin_required
def edit_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)

    if request.method == 'POST':
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            messages.success(request, "Internship updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = InternshipForm(instance=internship)

    return render(request, 'core/internship_form.html', {
        'form': form,
        'title': 'Edit Internship'
    })


@admin_required
def delete_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)

    if request.method == 'POST':
        internship.delete()
        messages.success(request, "Internship deleted successfully!")
        return redirect('admin_dashboard')

    return render(request, 'core/confirm_delete.html', {
        'object': internship,
        'url': 'admin_dashboard'
    })


@admin_required
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')

        if status in dict(Application.STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(request, "Application status updated!")

    return redirect('admin_dashboard')


# ================= STUDENT ================= #

@student_required
def student_dashboard(request):
    applications = Application.objects.select_related('internship').filter(user=request.user)

    total = applications.count()
    accepted = applications.filter(status='Accepted').count()
    rejected = applications.filter(status='Rejected').count()
    pending = applications.filter(status__in=['Pending', 'Applied']).count()

    return render(request, 'core/student_dashboard.html', {
        'applications': applications,
        'stats': {
            'total': total,
            'accepted': accepted,
            'rejected': rejected,
            'pending': pending
        }
    })


@student_required
def student_internships(request):
    internships = Internship.objects.all()
    return render(request, 'core/student_internships.html', {'internships': internships})


@student_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)

    if Application.objects.filter(user=request.user, internship=internship).exists():
        messages.error(request, "You have already applied for this internship.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.internship = internship
            application.save()

            messages.success(request, "Application submitted successfully!")
            return redirect('student_dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'core/application_form.html', {
        'form': form,
        'internship': internship,
        'title': 'Apply for Internship'
    })


@student_required
def edit_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    
    if application.status in ['Accepted', 'Rejected']:
        messages.error(request, "You cannot edit an application that has already been reviewed.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)

        if form.is_valid():
            form.save()
            messages.success(request, "Application updated successfully!")
            return redirect('student_dashboard')
    else:
        form = ApplicationForm(instance=application)

    return render(request, 'core/application_form.html', {
        'form': form,
        'internship': application.internship,
        'title': 'Edit Application'
    })


@student_required
def withdraw_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == 'POST':
        application.delete()
        messages.success(request, "Application withdrawn successfully!")
        return redirect('student_dashboard')

    return render(request, 'core/confirm_delete.html', {
        'object': application,
        'url': 'student_dashboard'
    })