
# user/views.py

import os
import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm, ProfilePicForm
from .models import Profile


# ==========================================
# REGISTER
# ==========================================

def register_view(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            password = form.cleaned_data.get("password")
            phone_number = form.cleaned_data.get("phone_number")
            address = form.cleaned_data.get("address")

            # ----------------------------------
            # Password length
            # ----------------------------------

            if len(password) < 8 or len(password) > 20:

                messages.error(
                    request,
                    "Password must be between 8 and 20 characters."
                )

                return render(
                    request,
                    "user/register.html",
                    {"form": form}
                )

            # ----------------------------------
            # Password special character
            # ----------------------------------

            special_char_pattern = re.compile(
                r"[@_!#$%^&*()<>?/\|}{~:]"
            )

            if not special_char_pattern.search(password):

                messages.error(
                    request,
                    "Password must contain at least one special character."
                )

                return render(
                    request,
                    "user/register.html",
                    {"form": form}
                )

            # ----------------------------------
            # Address length
            # ----------------------------------

            if address and len(address) > 200:

                messages.error(
                    request,
                    "Address is too long. Maximum 200 characters."
                )

                return render(
                    request,
                    "user/register.html",
                    {"form": form}
                )

            # ----------------------------------
            # Phone duplicate check
            # ----------------------------------

            if Profile.objects.filter(
                phone_number=phone_number
            ).exists():

                messages.error(
                    request,
                    "This phone number is already registered."
                )

                return render(
                    request,
                    "user/register.html",
                    {"form": form}
                )

            # ----------------------------------
            # Create User
            # ----------------------------------

            user = form.save(commit=False)

            user.set_password(password)

            user.save()

            # ----------------------------------
            # Get / create profile
            # ----------------------------------

            profile, created = Profile.objects.get_or_create(
                user=user
            )

            profile.fullName = form.cleaned_data.get("fullName")
            profile.phone_number = phone_number
            profile.address = address
            profile.gender = form.cleaned_data.get("gender")

            if form.cleaned_data.get("profile_pic"):

                profile.profile_pic = form.cleaned_data.get(
                    "profile_pic"
                )

            profile.save()

            # ----------------------------------
            # Login automatically
            # ----------------------------------

            user.backend = (
                "user.backends.EmailOrUsernameModelBackend"
            )

            login(request, user)

            messages.success(
                request,
                f"Welcome, {profile.fullName or user.username}! "
                "Your account has been created successfully."
            )

            return redirect("home")

        else:

            # Show form errors
            for field, errors in form.errors.items():

                for error in errors:

                    messages.error(
                        request,
                        error
                    )

    else:

        form = RegisterForm()

    return render(
        request,
        "user/register.html",
        {
            "form": form
        }
    )


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username_or_email = form.cleaned_data.get(
                "username"
            )

            password = form.cleaned_data.get(
                "password"
            )

            # ----------------------------------
            # Authenticate
            # ----------------------------------

            user = authenticate(
                request,
                username=username_or_email,
                password=password
            )

            # ----------------------------------
            # Login successful
            # ----------------------------------

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome back, {user.username}!"
                )

                return redirect("home")

            # ----------------------------------
            # Login failed
            # ----------------------------------

            messages.error(
                request,
                "Invalid username/email or password."
            )

    else:

        form = LoginForm()

    return render(
        request,
        "user/login.html",
        {
            "form": form
        }
    )


# ==========================================
# LOGOUT
# ==========================================

def logout_view(request):

    logout(request)

    messages.info(
        request,
        "You have been logged out."
    )

    return redirect("home")


# ==========================================
# DASHBOARD
# ==========================================

@login_required
def dashboard(request):

    return render(
        request,
        "user/dashboard.html"
    )


# ==========================================
# UPDATE PROFILE PICTURE
# ==========================================

@login_required
def update_profile_pic(request):

    if request.method == "POST":

        form = ProfilePicForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if form.is_valid():

            profile = request.user.profile

            # Delete old profile picture
            if (
                profile.profile_pic
                and profile.profile_pic.name
                and not profile.profile_pic.name.endswith(
                    "default.jpg"
                )
            ):

                old_path = profile.profile_pic.path

                if os.path.exists(old_path):

                    try:
                        os.remove(old_path)

                    except OSError:
                        pass

            form.save()

            messages.success(
                request,
                "Profile picture updated successfully!"
            )

        else:

            messages.error(
                request,
                "Failed to update. Please select a valid image."
            )

    return redirect("user:dashboard")

