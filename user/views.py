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

            password = form.cleaned_data["password"]

            # Create Django User
            user = form.save(commit=False)

            user.set_password(password)

            user.save()

            # Create/Get Profile
            profile = Profile.objects.get_or_create(
                user=user
            )[0]

            profile.fullName = form.cleaned_data["fullName"]
            profile.phone_number = form.cleaned_data["phone_number"]
            profile.address = form.cleaned_data["address"]
            profile.gender = form.cleaned_data["gender"]

            # Profile picture
            if form.cleaned_data.get("profile_pic"):

                profile.profile_pic = form.cleaned_data[
                    "profile_pic"
                ]

            # Generate 6-digit verification code
            verification_code = str(
                random.randint(100000, 999999)
            )

            profile.verification_code = verification_code
            profile.email_verified = False

            profile.save()

            # ==========================================
            # SEND VERIFICATION EMAIL
            # ==========================================

            send_mail(
                subject="TrustyShop Email Verification",

                message=f"""
Hello {user.username},

Welcome to TrustyShop!

Your verification code is:

{verification_code}

Please enter this code on the verification page.

Thank you,
TrustyShop Team
""",

                from_email=None,

                recipient_list=[
                    user.email
                ],

                fail_silently=False,
            )

            # Save user ID for verification page
            request.session[
                "verification_user_id"
            ] = user.id

            messages.success(
                request,
                "Registration successful! "
                "A verification code has been sent "
                "to your email."
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

    return redirect("welcome")


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

    # Don't allow already logged-in users
    if request.user.is_authenticated:

        return redirect("home")

    # Get user ID from session
    user_id = request.session.get(
        "verification_user_id"
    )

    if not user_id:

        messages.error(
            request,
            "Verification session expired. "
            "Please register again."
        )

        return redirect(
            "user:register"
        )

    # Find user
    try:

        user = User.objects.get(
            id=user_id
        )

        profile = user.profile

    except User.DoesNotExist:

        messages.error(
            request,
            "User account not found."
        )

        return redirect(
            "user:register"
        )

    # ==========================================
    # VERIFY CODE
    # ==========================================

    if request.method == "POST":

        form = EmailVerificationForm(
            request.POST
        )

        if form.is_valid():

            code = form.cleaned_data[
                "code"
            ]

            # Correct code
            if profile.verification_code == code:

                profile.email_verified = True

                profile.verification_code = None

                profile.save()

                # Remove verification session
                request.session.pop(
                    "verification_user_id",
                    None
                )

                # Specify authentication backend
                user.backend = (
                    "user.backends.EmailOrUsernameModelBackend"
                )

                # Log user in
                login(
                    request,
                    user
                )

                messages.success(
                    request,
                    "Email verified successfully! "
                    "Welcome to TrustyShop."
                )

                return redirect(
                    "home"
                )

            # Incorrect code
            else:

                messages.error(
                    request,
                    "Invalid verification code."
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