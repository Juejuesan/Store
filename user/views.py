import os
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
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
            phone_number = form.cleaned_data.get('phone_number')

            if len(password) < 8 or len(password) > 20:
                messages.error(request, "Password must be at least 8 characters long!")
                return render(request, 'user/register.html', {'form': form})

            special_char_pattern = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
            if not special_char_pattern.search(password):
                messages.error(request, "Password must contain at least one special character (e.g., @, #, $, %)! ")
                return render(request, 'user/register.html', {'form': form})

            if len(address) > 200:
                messages.error(request, "Address is too long! (Maximum 200 characters allowed)")
                return render(request, 'user/register.html', {'form': form})

            if Profile.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "This phone number is already registered!")
                return render(request, 'user/register.html', {'form': form})

            user = form.save(commit=False)
            user.set_password(password)
            user.save()

            # Save profile
            profile = user.profile
            profile.fullName = form.cleaned_data['fullName']
            profile.phone_number = phone_number
            profile.address = address
            profile.gender = form.cleaned_data['gender']
            if form.cleaned_data.get('profile_pic'):
                profile.profile_pic = form.cleaned_data['profile_pic']
            profile.save()

            # Auto login after registration
            user.backend = 'user.backends.EmailOrUsernameModelBackend'
            login(request, user)

            messages.success(request, f'Welcome, {profile.fullName or user.username}! Your account has been created.')
            return redirect('user:dashboard')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})


# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = None

        # First try to authenticate directly with username
        user = authenticate(request, username=username_or_email, password=password)

        # If direct authentication fails, try looking up by email (case-insensitive)
        if user is None:
            try:
                user_obj = User.objects.filter(email__iexact=username_or_email).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)
            except Exception:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'user/login.html')


# LOGOUT VIEW
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('/')


# DASHBOARD VIEW
@login_required
def dashboard(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile

        fullName = request.POST.get('fullName', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number', '').strip()
        address = request.POST.get('address', '').strip()
        profile_pic = request.FILES.get('profile_pic')

        # 1. Validate Phone Number (Digits only, length between 9 and 11)
        if phone_number:
            if not phone_number.isdigit():
                messages.error(request, 'Phone number must contain digits only!')
                return redirect('user:dashboard')

            if len(phone_number) < 9 or len(phone_number) > 11:
                messages.error(request, 'Phone number must be between 9 and 11 digits!')
                return redirect('user:dashboard')

            if phone_number != profile.phone_number and Profile.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'This phone number is already registered to another user!')
                return redirect('user:dashboard')

            profile.phone_number = phone_number
        else:
            profile.phone_number = ''

        # 2. Validate Gender (Male or Female only)
        if gender in ['M', 'F']:
            profile.gender = gender

        # 3. Check unique username constraint if modified
        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken!')
                return redirect('user:dashboard')
            user.username = username

        # 4. Check unique email constraint if modified
        if email and email != user.email:
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'Email is already in use by another account!')
                return redirect('user:dashboard')
            user.email = email

        # Update User model
        user.save()

        # Update Profile model
        profile.fullName = fullName
        profile.address = address

        # Handle profile picture replacement
        if profile_pic:
            if profile.profile_pic and not profile.profile_pic.name.endswith('default.jpg'):
                old_path = profile.profile_pic.path
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except OSError:
                        pass
            profile.profile_pic = profile_pic

        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('user:dashboard')

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