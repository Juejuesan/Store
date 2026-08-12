
import os
import random

from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone

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

            # =====================================================
            # GENERATE 6-DIGIT VERIFICATION CODE
            # =====================================================

            verification_code = str(
                random.randint(100000, 999999)
            )

            # =====================================================
            # STORE REGISTRATION DATA IN SESSION
            # =====================================================

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

            # =====================================================
            # TEMPORARILY SAVE PROFILE PICTURE
            # =====================================================

            profile_pic = form.cleaned_data.get(
                "profile_pic"
            )

            if profile_pic:

                temp_path = default_storage.save(
                    f"pending_profile_pics/{profile_pic.name}",
                    profile_pic,
                )

                request.session[
                    "pending_profile_pic_path"
                ] = temp_path

            else:

                request.session.pop(
                    "pending_profile_pic_path",
                    None
                )

            # =====================================================
            # SEND VERIFICATION EMAIL
            # =====================================================

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

                from_email=settings.DEFAULT_FROM_EMAIL,

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


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username_or_email = (
                form.cleaned_data["username"].strip()
            )

            password = form.cleaned_data["password"]

            remember_me = form.cleaned_data[
                "remember_me"
            ]

            # =================================================
            # AUTHENTICATE USER
            # =================================================

            user = authenticate(
                request=request,
                username=username_or_email,
                password=password,
            )

            # =================================================
            # SUCCESSFUL LOGIN
            # =================================================

            if user is not None:

                login(
                    request,
                    user
                )

                # =================================================
                # REMEMBER ME
                # =================================================

                if remember_me:

                    request.session.set_expiry(
                        60 * 60 * 24 * 30
                    )

                else:

                    request.session.set_expiry(0)

                # =================================================
                # GET PROFILE
                # =================================================

                profile = getattr(
                    user,
                    "profile",
                    None,
                )

                if profile and profile.fullName:

                    full_name = profile.fullName

                else:

                    full_name = user.username

                messages.success(
                    request,
                    f"Welcome back, {full_name}!"
                )

                return redirect(
                    "home"
                )

            # =================================================
            # FAILED LOGIN
            # =================================================

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


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    messages.info(
        request,
        "You have been logged out."
    )

    return redirect(
        "welcome"
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    return render(
        request,
        "user/dashboard.html"
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

            # =================================================
            # DELETE OLD PROFILE PICTURE
            # =================================================

            if (
                profile.profile_pic
                and profile.profile_pic.name
                and not profile.profile_pic.name.endswith(
                    "default.jpg"
                )
            ):

                try:

                    old_path = profile.profile_pic.path

                    if os.path.exists(old_path):

                        os.remove(old_path)

                except (
                    ValueError,
                    OSError,
                ):

                    pass

            # =================================================
            # SAVE NEW PROFILE PICTURE
            # =================================================

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


# =========================================================
# VERIFY EMAIL
# =========================================================

def verify_email(request):

    # =========================================================
    # GET PENDING REGISTRATION
    # =========================================================

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

    # =========================================================
    # POST
    # =========================================================

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

            # =================================================
            # CORRECT VERIFICATION CODE
            # =================================================

            if entered_code == correct_code:

                # =============================================
                # CREATE USER
                # =============================================

                user = User.objects.create_user(

                    username=pending[
                        "username"
                    ],

                    email=pending[
                        "email"
                    ],

                    password=pending[
                        "password"
                    ],
                )

                # =============================================
                # CREATE PROFILE
                # =============================================

                profile, created = (
                    Profile.objects.get_or_create(
                        user=user
                    )
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

                # =============================================
                # RESTORE PROFILE PICTURE
                # =============================================

                temp_pic_path = request.session.get(
                    "pending_profile_pic_path"
                )

                if temp_pic_path:

                    try:

                        if default_storage.exists(
                            temp_pic_path
                        ):

                            profile.profile_pic = (
                                temp_pic_path
                            )

                    except Exception:

                        pass

                # =============================================
                # EMAIL VERIFIED
                # =============================================

                profile.email_verified = True

                profile.verification_code = None

                profile.save()

                # =============================================
                # REMOVE TEMPORARY SESSION DATA
                # =============================================

                request.session.pop(
                    "pending_registration",
                    None
                )

                request.session.pop(
                    "pending_profile_pic_path",
                    None
                )

                # =============================================
                # LOGIN NEW USER
                # =============================================

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

            # =================================================
            # WRONG CODE
            # =================================================

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


# =========================================================
# FORGOT PASSWORD
# SEND OTP
# =========================================================

def forgot_password(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = ForgotPasswordForm(
            request.POST
        )

        if form.is_valid():

            email = form.cleaned_data[
                "email"
            ]

            user = User.objects.filter(
                email__iexact=email,
                is_active=True,
            ).first()

            # =================================================
            # SECURITY
            # Do not reveal whether email exists
            # =================================================

            if user:

                # =================================================
                # DELETE PREVIOUS UNUSED OTP
                # =================================================

                PasswordResetOTP.objects.filter(
                    user=user,
                    is_used=False,
                ).delete()

                # =================================================
                # GENERATE 6-DIGIT OTP
                # =================================================

                otp = str(
                    random.randint(
                        100000,
                        999999
                    )
                )

                # =================================================
                # OTP EXPIRATION
                # =================================================

                now = timezone.now()

                expires_at = (
                    now
                    + timedelta(minutes=5)
                )

                # =================================================
                # CREATE OTP
                # =================================================

                PasswordResetOTP.objects.create(

                    user=user,

                    otp=otp,

                    expires_at=expires_at,
                )

                # =================================================
                # SEND OTP EMAIL
                # =================================================

                send_mail(

                    subject=(
                        "TrustyShop Password Reset OTP"
                    ),

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

                    from_email=(
                        settings.DEFAULT_FROM_EMAIL
                    ),

                    recipient_list=[
                        user.email
                    ],

                    fail_silently=False,
                )

                # =================================================
                # STORE EMAIL IN SESSION
                # =================================================

                request.session[
                    "password_reset_email"
                ] = user.email

            # =================================================
            # SAME MESSAGE FOR SECURITY
            # =================================================

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
            "form": form
        }
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

            # =================================================
            # CHECK EMAIL
            # =================================================

            if (
                submitted_email.lower()
                != email.lower()
            ):

                form.add_error(
                    "email",
                    "This email does not match "
                    "the reset request."
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

                # =================================================
                # GET LATEST UNUSED OTP
                # =================================================

                reset_otp = (
                    PasswordResetOTP.objects
                    .filter(
                        user=user,
                        is_used=False,
                    )
                    .order_by("-created_at")
                    .first()
                )

                # =================================================
                # OTP DOES NOT EXIST
                # =================================================

                if not reset_otp:

                    form.add_error(
                        "otp",
                        "OTP is invalid. "
                        "Please request a new OTP."
                    )

                # =================================================
                # OTP EXPIRED
                # =================================================

                elif reset_otp.is_expired():

                    reset_otp.delete()

                    form.add_error(
                        "otp",
                        "OTP has expired. "
                        "Please request a new OTP."
                    )

                # =================================================
                # OTP INCORRECT
                # =================================================

                elif reset_otp.otp != otp:

                    form.add_error(
                        "otp",
                        "Incorrect OTP."
                    )

                # =================================================
                # OTP CORRECT
                # =================================================

                else:

                    request.session[
                        "password_reset_user_id"
                    ] = user.id

                    request.session[
                        "password_reset_otp_id"
                    ] = reset_otp.id

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
        }
    )


# =========================================================
# RESET PASSWORD
# =========================================================

def reset_password(request):

    if request.user.is_authenticated:
        return redirect("home")

    # =========================================================
    # CHECK OTP VERIFICATION
    # =========================================================

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

    # =========================================================
    # GET SESSION DATA
    # =========================================================

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

    # =========================================================
    # GET USER
    # =========================================================

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

    # =========================================================
    # GET OTP
    # =========================================================

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

    # =========================================================
    # CHECK OTP EXPIRATION AGAIN
    # =========================================================

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
            "OTP has expired. "
            "Please request a new OTP."
        )

        return redirect(
            "user:forgot_password"
        )

    # =========================================================
    # GET RESET PASSWORD PAGE
    # =========================================================

    if request.method == "GET":

        form = ResetPasswordForm()

        return render(
            request,
            "user/reset_password.html",
            {
                "form": form
            }
        )

    # =========================================================
    # POST RESET PASSWORD
    # =========================================================

    form = ResetPasswordForm(
        request.POST
    )

    if not form.is_valid():

        return render(
            request,
            "user/reset_password.html",
            {
                "form": form
            }
        )

    new_password = form.cleaned_data[
        "new_password"
    ]

    # =========================================================
    # HASH NEW PASSWORD
    # =========================================================

    user.set_password(
        new_password
    )

    user.save(
        update_fields=[
            "password"
        ]
    )

    # =========================================================
    # VERIFY PASSWORD WAS SAVED
    # =========================================================

    user.refresh_from_db()

    if not user.check_password(
        new_password
    ):

        messages.error(
            request,
            "Password could not be saved. "
            "Please try again."
        )

        return render(
            request,
            "user/reset_password.html",
            {
                "form": form
            }
        )

    # =========================================================
    # MARK OTP AS USED
    # =========================================================

    reset_otp.is_used = True

    reset_otp.save(
        update_fields=[
            "is_used"
        ]
    )

    # =========================================================
    # REMOVE RESET SESSION DATA
    # =========================================================

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

    # =========================================================
    # DELETE USED OTP
    # =========================================================

    reset_otp.delete()

    # =========================================================
    # SUCCESS
    # =========================================================

    messages.success(
        request,
        "Your password has been changed successfully. "
        "You can now login with your new password."
    )

    return redirect(
        "user:login"
    )

