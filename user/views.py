import os
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import (
    RegisterForm,
    LoginForm,
    ProfilePicForm,
    EmailVerificationForm,
)
from .models import Profile
from django.db.models import Q

# ==========================================
# REGISTER
# ==========================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            # ==========================================
            # GENERATE EXACTLY 6 DIGIT CODE
            # ==========================================

            verification_code = str(
                random.randint(100000, 999999)
            )

            # ==========================================
            # STORE REGISTRATION DATA TEMPORARILY
            # ==========================================

            request.session["pending_registration"] = {

                "username": form.cleaned_data["username"],

                "email": form.cleaned_data["email"],

                "password": form.cleaned_data["password"],

                "fullName": form.cleaned_data["fullName"],

                "phone_number": form.cleaned_data["phone_number"],

                "address": form.cleaned_data["address"],

                "gender": form.cleaned_data["gender"],

                "verification_code": verification_code,
            }

            # ==========================================
            # PROFILE PICTURE
            # ==========================================
            #
            # Django sessions cannot store uploaded files.
            #
            # Therefore, for now we will temporarily store
            # the uploaded image separately.
            #

            if form.cleaned_data.get("profile_pic"):

                profile_pic = form.cleaned_data[
                    "profile_pic"
                ]

                # Store uploaded file temporarily
                request.session["pending_profile_pic_name"] = (
                    profile_pic.name
                )

                # NOTE:
                # We will handle the actual file storage
                # in the next step.

            # ==========================================
            # SEND VERIFICATION EMAIL
            # ==========================================

            send_mail(

                subject="TrustyShop Email Verification",

                message=f"""
Hello {form.cleaned_data["username"]},

Welcome to TrustyShop!

Your verification code is:

{verification_code}

Please enter this 6-digit code to complete
your TrustyShop registration.

Thank you,
TrustyShop Team
""",

                from_email=None,

                recipient_list=[
                    form.cleaned_data["email"]
                ],

                fail_silently=False,
            )

            messages.success(
                request,
                "Your registration information is valid. "
                "Please enter the 6-digit code sent "
                "to your email to complete registration."
            )

            return redirect(
                "user:verify_email"
            )

        else:

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

        form = LoginForm(
            request.POST
        )

        if form.is_valid():

            username_or_email = (
                form.cleaned_data.get(
                    "username"
                )
            )

            password = (
                form.cleaned_data.get(
                    "password"
                )
            )

            # Authenticate
            user = authenticate(
                request,
                username=username_or_email,
                password=password
            )

            # Login successful
            if user is not None:

                login(
                    request,
                    user
                )

                messages.success(
                    request,
                    f"Welcome back, {user.username}!"
                )

                return redirect("home")

            # Login failed
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
                "Failed to update. "
                "Please select a valid image."
            )

    return redirect(
        "user:dashboard"
    )


# ==========================================
# VERIFY EMAIL
# ==========================================

def verify_email(request):

    # ==========================================
    # GET PENDING REGISTRATION
    # ==========================================

    pending = request.session.get(
        "pending_registration"
    )

    if not pending:

        messages.error(
            request,
            "Your registration session has expired. "
            "Please register again."
        )

        return redirect(
            "user:register"
        )

    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        form = EmailVerificationForm(
            request.POST
        )

        if form.is_valid():

            entered_code = form.cleaned_data[
                "code"
            ]

            correct_code = pending.get(
                "verification_code"
            )

            # ======================================
            # CORRECT 6 DIGITS
            # ======================================

            if entered_code == correct_code:

                # ==================================
                # CREATE USER ONLY NOW
                # ==================================

                user = User.objects.create_user(

                    username=pending["username"],

                    email=pending["email"],

                    password=pending["password"]
                )

                # ==================================
                # CREATE PROFILE
                # ==================================

                profile = Profile.objects.get(
                    user=user
                )

                profile.fullName = pending[
                    "fullName"
                ]

                profile.phone_number = pending[
                    "phone_number"
                ]

                profile.address = pending[
                    "address"
                ]

                profile.gender = pending[
                    "gender"
                ]

                # ==================================
                # EMAIL IS VERIFIED
                # ==================================

                profile.email_verified = True

                profile.verification_code = None

                profile.save()

                # ==================================
                # DELETE TEMPORARY REGISTRATION DATA
                # ==================================

                request.session.pop(
                    "pending_registration",
                    None
                )

                request.session.pop(
                    "pending_profile_pic_name",
                    None
                )

                # ==================================
                # LOGIN NEW USER
                # ==================================

                user.backend = (
                    "user.backends.EmailOrUsernameModelBackend"
                )

                login(
                    request,
                    user
                )

                messages.success(
                    request,
                    "Registration completed successfully! "
                    "Welcome to TrustyShop."
                )

                return redirect(
                    "home"
                )

            # ======================================
            # WRONG CODE
            # ======================================

            messages.error(
                request,
                "Incorrect verification code. "
                "Please enter the 6-digit code "
                "sent to your email."
            )

    else:

        form = EmailVerificationForm()

    return render(
        request,
        "user/verify_email.html",
        {
            "form": form
        }
    )