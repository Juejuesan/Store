import re
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ProfilePicForm


# REGISTER VIEW
def register_view(request):
    if request.user.is_authenticated:
        return redirect('user:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():

            password = form.cleaned_data.get('password')
            address = form.cleaned_data.get('address', '')


            if len(password) != 8:
                messages.error(request, "Password must be exactly 8 characters long!")
                return render(request, 'user/register.html', {'form': form})


            special_char_pattern = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
            if not special_char_pattern.search(password):
                messages.error(request, "Password must contain at least one special character (e.g., @, #, $, %)! ")
                return render(request, 'user/register.html', {'form': form})


            if len(address) > 200:
                messages.error(request, "Address is too long! (Maximum 200 characters allowed)")
                return render(request, 'user/register.html', {'form': form})


            user = form.save(commit=False)
            user.set_password(password)
            user.save()


            user.profile.phone_number = form.cleaned_data['phone_number']
            user.profile.address = address
            user.profile.gender = form.cleaned_data['gender']
            if form.cleaned_data.get('profile_pic'):
                user.profile.profile_pic = form.cleaned_data['profile_pic']
            user.profile.save()

            login(request, user)
            messages.success(request, f'Welcome, {user.first_name or user.username}!')
            return redirect('user:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})


# LOGIN VIEW
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']


            if len(password) != 8:
                messages.error(request, 'Invalid username/email or password.')
                return render(request, 'user/login.html', {'form': form})

            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('user:dashboard')
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})


# LOGOUT VIEW
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('/')


# DASHBOARD VIEW
@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html')


# UPDATE PROFILE PICTURE VIEW
@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = request.user.profile

            if profile.profile_pic and not profile.profile_pic.name.endswith('default.jpg'):
                old_path = profile.profile_pic.path
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except OSError:
                        pass

            form.save()
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.error(request, 'Failed to update. Please select a valid image.')

    return redirect('user:dashboard')