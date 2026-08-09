from .models import Profile, PasswordResetOTP
from datetime import timedelta
import random
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
import os
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import (
    RegisterForm,
    LoginForm,
    ProfilePicForm,
    EmailVerificationForm,
    ForgotPasswordForm,
    OTPVerificationForm,
    ResetPasswordForm,
)

from .models import (
    Profile,
    PasswordResetOTP,
)
User = get_user_model()



# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            password = form.cleaned_data["password"]

            user = form.save(commit=False)

            # IMPORTANT:
            # Always hash the password.
            user.set_password(password)

            user.save()

            profile, created = Profile.objects.get_or_create(
                user=user
            )

            profile.fullName = form.cleaned_data["fullName"]
            profile.phone_number = form.cleaned_data["phone_number"]
            profile.address = form.cleaned_data["address"]
            profile.gender = form.cleaned_data["gender"]

            profile_pic = form.cleaned_data.get("profile_pic")

            if profile_pic:
                profile.profile_pic = profile_pic

            verification_code = str(
                random.randint(100000, 999999)
            )

            profile.verification_code = verification_code
            profile.email_verified = False

            profile.save()

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
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            request.session["verification_user_id"] = user.id

            messages.success(
                request,
                "Registration successful! "
                "A verification code has been sent to your email.",
            )

            return redirect("user:verify_email")

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    else:
        form = RegisterForm()

    return render(
        request,
        "user/register.html",
        {"form": form},
    )


# =========================================================
# LOGIN
# =========================================================
def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username_or_email = form.cleaned_data["username"].strip()
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data["remember_me"]

            print("\n" + "=" * 60)
            print("LOGIN DEBUG")
            print("Entered username/email:", repr(username_or_email))
            print("Password length:", len(password))

            # Find user directly
            try:
                test_user = User.objects.get(
                    Q(username__iexact=username_or_email)
                    | Q(email__iexact=username_or_email)
                )

                print("FOUND USER:")
                print("ID:", test_user.id)
                print("Username:", test_user.username)
                print("Email:", test_user.email)
                print("Active:", test_user.is_active)

                print(
                    "DIRECT PASSWORD CHECK:",
                    test_user.check_password(password)
                )

            except User.DoesNotExist:

                print("USER NOT FOUND")

            except User.MultipleObjectsReturned:

                print("MULTIPLE USERS FOUND")

            # Django authenticate
            user = authenticate(
                request=request,
                username=username_or_email,
                password=password,
            )

            print("AUTHENTICATE RESULT:", user)
            print("=" * 60 + "\n")

            if user is not None:

                login(request, user)

                if remember_me:
                    request.session.set_expiry(
                        60 * 60 * 24 * 30
                    )
                else:
                    request.session.set_expiry(0)

                profile = getattr(
                    user,
                    "profile",
                    None,
                )

                full_name = (
                    profile.fullName
                    if profile and profile.fullName
                    else user.username
                )

                messages.success(
                    request,
                    f"Welcome back, {full_name}!",
                )

                return redirect("home")

            messages.error(
                request,
                "Invalid username/email or password.",
            )

    else:
        form = LoginForm()

    return render(
        request,
        "user/login.html",
        {"form": form},
    )
# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    messages.info(
        request,
        "You have been logged out.",
    )

    return redirect("welcome")


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    return render(
        request,
        "user/dashboard.html",
    )


# =========================================================
# UPDATE PROFILE PICTURE
# =========================================================

@login_required
def update_profile_pic(request):

    if request.method == "POST":

        form = ProfilePicForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )

        if form.is_valid():

            profile = request.user.profile

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
                "Profile picture updated successfully!",
            )

        else:

            messages.error(
                request,
                "Failed to update. Please select a valid image.",
            )

    return redirect("user:dashboard")


# =========================================================
# VERIFY EMAIL
# =========================================================

def verify_email(request):

    if request.user.is_authenticated:
        return redirect("home")

    user_id = request.session.get(
        "verification_user_id"
    )

    if not user_id:

        messages.error(
            request,
            "Verification session expired. Please register again.",
        )

        return redirect("user:register")

    try:

        user = User.objects.get(
            id=user_id
        )

        profile = user.profile

    except (
        User.DoesNotExist,
        Profile.DoesNotExist,
    ):

        messages.error(
            request,
            "User account not found.",
        )

        return redirect("user:register")

    if request.method == "POST":

        form = EmailVerificationForm(
            request.POST
        )

        if form.is_valid():

            code = form.cleaned_data["code"]

            if profile.verification_code == code:

                profile.email_verified = True
                profile.verification_code = None

                profile.save(
                    update_fields=[
                        "email_verified",
                        "verification_code",
                    ]
                )

                request.session.pop(
                    "verification_user_id",
                    None
                )

                user.backend = (
                    "user.backends.EmailOrUsernameModelBackend"
                )

                login(
                    request,
                    user,
                )

                messages.success(
                    request,
                    "Email verified successfully! "
                    "Welcome to TrustyShop.",
                )

                return redirect("home")

            messages.error(
                request,
                "Invalid verification code.",
            )

    else:

        form = EmailVerificationForm()

    return render(
        request,
        "user/verify_email.html",
        {"form": form},
    )
# =========================================================
# FORGOT PASSWORD - SEND OTP
# =========================================================

def forgot_password(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            user = User.objects.filter(
                email__iexact=email,
                is_active=True,
            ).first()

            # -------------------------------------------------
            # SECURITY:
            # Don't reveal whether email exists.
            # -------------------------------------------------

            if user:

                # Delete any previous unused OTPs
                PasswordResetOTP.objects.filter(
                    user=user,
                    is_used=False,
                ).delete()

                # Generate 6-digit OTP
                otp = str(
                    random.randint(100000, 999999)
                )

                # Current time
                now = timezone.now()

                # OTP expires after 5 minutes
                expires_at = now + timedelta(
                    minutes=5
                )

                # Save OTP
                PasswordResetOTP.objects.create(
                    user=user,
                    otp=otp,
                    expires_at=expires_at,
                )

                # Send OTP email
                send_mail(
                    subject="TrustyShop Password Reset OTP",

                    message=f"""
Hello {user.username},

We received a request to reset your TrustyShop password.

Your password reset OTP is:

{otp}

This OTP will expire in 5 minutes.

If you did not request a password reset,
please ignore this email.

TrustyShop Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        user.email
                    ],

                    fail_silently=False,
                )

                # Store email in session
                request.session[
                    "password_reset_email"
                ] = user.email

            messages.success(
                request,
                "If an account exists with that email, "
                "a 6-digit OTP has been sent."
            )

            return redirect(
                "user:verify_reset_otp"
            )

    else:

        form = ForgotPasswordForm()

    return render(
        request,
        "user/forgot_password.html",
        {
            "form": form,
        },
    )

# =========================================================
# VERIFY PASSWORD RESET OTP
# =========================================================

def verify_reset_otp(request):

    if request.user.is_authenticated:
        return redirect("home")

    email = request.session.get(
        "password_reset_email"
    )

    if not email:

        messages.error(
            request,
            "Password reset session expired. "
            "Please request a new OTP."
        )

        return redirect(
            "user:forgot_password"
        )

    if request.method == "POST":

        form = OTPVerificationForm(
            request.POST
        )

        if form.is_valid():

            submitted_email = (
                form.cleaned_data["email"]
            )

            otp = form.cleaned_data["otp"]

            # Make sure email matches session
            if submitted_email.lower() != email.lower():

                form.add_error(
                    "email",
                    "This email does not match the reset request."
                )

            else:

                user = User.objects.filter(
                    email__iexact=email,
                    is_active=True,
                ).first()

                if not user:

                    messages.error(
                        request,
                        "Account not found."
                    )

                    return redirect(
                        "user:forgot_password"
                    )

                # Get latest unused OTP
                reset_otp = (
                    PasswordResetOTP.objects
                    .filter(
                        user=user,
                        is_used=False,
                    )
                    .order_by("-created_at")
                    .first()
                )

                print("=" * 60)
                print("OTP DEBUG")
                print("Submitted OTP:", repr(otp))
                print("Database OTP:", repr(reset_otp.otp if reset_otp else None))
                print("Created:", reset_otp.created_at if reset_otp else None)
                print("Expires:", reset_otp.expires_at if reset_otp else None)
                print("Current time:", timezone.now())
                print("Expired:", reset_otp.is_expired() if reset_otp else None)
                print("Used:", reset_otp.is_used if reset_otp else None)
                print("=" * 60)

                # No OTP
                if not reset_otp:

                    form.add_error(
                        "otp",
                        "OTP is invalid. Please request a new OTP."
                    )

                # OTP expired
                elif reset_otp.is_expired():

                    reset_otp.delete()

                    form.add_error(
                        "otp",
                        "OTP has expired. Please request a new OTP."
                    )

                # OTP incorrect
                elif reset_otp.otp != otp:

                    form.add_error(
                        "otp",
                        "Incorrect OTP."
                    )

                # OTP correct
                else:

                    # Store verified user ID
                    request.session[
                        "password_reset_user_id"
                    ] = user.id

                    # Store OTP ID
                    request.session[
                        "password_reset_otp_id"
                    ] = reset_otp.id

                    # Mark that OTP was verified
                    request.session[
                        "password_reset_verified"
                    ] = True

                    return redirect(
                        "user:reset_password"
                    )

    else:

        form = OTPVerificationForm(
            initial={
                "email": email
            }
        )

    return render(
        request,
        "user/verify_reset_otp.html",
        {
            "form": form,
            "email": email,
        },
    )


# =========================================================
# RESET PASSWORD
# =========================================================

def reset_password(request):

    if request.user.is_authenticated:
        return redirect("home")

    # -----------------------------------------------------
    # Check OTP verification session
    # -----------------------------------------------------

    if not request.session.get(
        "password_reset_verified"
    ):

        messages.error(
            request,
            "Please verify your OTP first."
        )

        return redirect(
            "user:forgot_password"
        )

    user_id = request.session.get(
        "password_reset_user_id"
    )

    otp_id = request.session.get(
        "password_reset_otp_id"
    )

    if not user_id or not otp_id:

        messages.error(
            request,
            "Password reset session expired."
        )

        return redirect(
            "user:forgot_password"
        )

    # -----------------------------------------------------
    # Get user
    # -----------------------------------------------------

    try:

        user = User.objects.get(
            id=user_id,
            is_active=True,
        )

    except User.DoesNotExist:

        messages.error(
            request,
            "User account could not be found."
        )

        return redirect(
            "user:forgot_password"
        )

    # -----------------------------------------------------
    # Get OTP
    # -----------------------------------------------------

    try:

        reset_otp = PasswordResetOTP.objects.get(
            id=otp_id,
            user=user,
            is_used=False,
        )

    except PasswordResetOTP.DoesNotExist:

        messages.error(
            request,
            "OTP is no longer valid."
        )

        return redirect(
            "user:forgot_password"
        )

    # -----------------------------------------------------
    # Check expiration AGAIN
    # -----------------------------------------------------

    if reset_otp.is_expired():

        reset_otp.delete()

        request.session.pop(
            "password_reset_verified",
            None
        )

        request.session.pop(
            "password_reset_user_id",
            None
        )

        request.session.pop(
            "password_reset_otp_id",
            None
        )

        messages.error(
            request,
            "OTP has expired. Please request a new OTP."
        )

        return redirect(
            "user:forgot_password"
        )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == "GET":

        form = ResetPasswordForm()

        return render(
            request,
            "user/reset_password.html",
            {
                "form": form,
            },
        )

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    form = ResetPasswordForm(
        request.POST
    )

    if not form.is_valid():

        return render(
            request,
            "user/reset_password.html",
            {
                "form": form,
            },
        )

    new_password = form.cleaned_data[
        "new_password"
    ]

    # -----------------------------------------------------
    # IMPORTANT:
    # set_password() hashes the password correctly.
    # -----------------------------------------------------

    user.set_password(
        new_password
    )

    user.save(
        update_fields=[
            "password"
        ]
    )

    # -----------------------------------------------------
    # Verify database password
    # -----------------------------------------------------

    user.refresh_from_db()

    if not user.check_password(
        new_password
    ):

        messages.error(
            request,
            "Password could not be saved. Please try again."
        )

        return render(
            request,
            "user/reset_password.html",
            {
                "form": form,
            },
        )

    # -----------------------------------------------------
    # OTP is now consumed
    # -----------------------------------------------------

    reset_otp.is_used = True

    reset_otp.save(
        update_fields=[
            "is_used"
        ]
    )

    # -----------------------------------------------------
    # Remove all reset session data
    # -----------------------------------------------------

    request.session.pop(
        "password_reset_verified",
        None
    )

    request.session.pop(
        "password_reset_user_id",
        None
    )

    request.session.pop(
        "password_reset_otp_id",
        None
    )

    request.session.pop(
        "password_reset_email",
        None
    )

    # -----------------------------------------------------
    # Delete used OTP
    # -----------------------------------------------------

    reset_otp.delete()

    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    messages.success(
        request,
        "Your password has been changed successfully. "
        "You can now login with your new password."
    )

    return redirect(
        "user:login"
    )