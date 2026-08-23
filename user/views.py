# =========================================================
# user/views.py
# =========================================================

from .forms import (
    RegisterForm,
    LoginForm,
    ProfilePicForm,
    ProfileEditForm,
    EmailVerificationForm,
    ForgotPasswordForm,
    OTPVerificationForm,
    ResetPasswordForm,
)

from posts.models import Post

import os
import random

from datetime import timedelta
from functools import wraps

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
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.utils import timezone

from wishlist.models import Wishlist

from .models import (
    Profile,
    PasswordResetOTP,
)


User = get_user_model()


# =========================================================
# SESSION CHECK DECORATOR
# =========================================================

def check_session_user(view_func):
    """
    Check whether the current session still belongs
    to the logged-in user.

    This helps prevent account switching problems
    between multiple browser tabs.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:

            session_user_id = request.session.get(
                "logged_in_user_id"
            )

            if (
                session_user_id
                and session_user_id != request.user.id
            ):

                logout(request)

                messages.warning(
                    request,
                    "Your session expired because your account "
                    "was changed in another tab. Please login again."
                )

                return redirect(
                    "user:login"
                )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper


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

            verification_code = str(
                random.randint(
                    100000,
                    999999,
                )
            )

            # =================================================
            # SAVE REGISTRATION DATA IN SESSION
            # =================================================

            request.session[
                "pending_registration"
            ] = {

                "username": form.cleaned_data[
                    "username"
                ],

                "email": form.cleaned_data[
                    "email"
                ],

                "password": form.cleaned_data[
                    "password"
                ],

                "fullName": form.cleaned_data[
                    "fullName"
                ],

                "phone_number": form.cleaned_data[
                    "phone_number"
                ],

                "gender": form.cleaned_data[
                    "gender"
                ],

                "verification_code": verification_code,
            }

            # =================================================
            # TEMPORARILY SAVE PROFILE PICTURE
            # =================================================

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
                    None,
                )

            # =================================================
            # SEND VERIFICATION EMAIL
            # =================================================

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
                        error,
                    )

    else:

        form = RegisterForm()

    return render(
        request,
        "user/register.html",
        {
            "form": form,
        },
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = LoginForm(
            request.POST
        )

        if form.is_valid():

            username_or_email = (
                form.cleaned_data[
                    "username"
                ].strip()
            )

            password = form.cleaned_data[
                "password"
            ]

            remember_me = form.cleaned_data[
                "remember_me"
            ]

            # =================================================
            # AUTHENTICATE
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
                    user,
                )

                request.session[
                    "logged_in_user_id"
                ] = user.id

                # =================================================
                # REMEMBER ME
                # =================================================

                if remember_me:

                    request.session.set_expiry(
                        60 * 60 * 24 * 30
                    )

                else:

                    request.session.set_expiry(
                        0
                    )

                # =================================================
                # PROFILE
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

                # =================================================
                # TERMS
                # =================================================

                if (
                    profile
                    and not profile.terms_accepted
                ):

                    request.session[
                        "show_terms_policy"
                    ] = True

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
            "form": form,
        },
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    request.session.pop(
        "logged_in_user_id",
        None,
    )

    logout(request)

    messages.info(
        request,
        "You have been logged out."
    )

    return redirect(
        "welcome"
    )


# =========================================================
# USER DASHBOARD
# =========================================================
#
# OWNER:
#   - Approved Posts
#   - Pending Posts
#   - Wishlist
#
# This view is for the logged-in user's own dashboard.
# =========================================================

@login_required
@check_session_user
def dashboard(request):

    # =====================================================
    # GET PROFILE
    # =====================================================

    profile = get_object_or_404(
        Profile,
        user=request.user,
    )

    # =====================================================
    # ALL USER POSTS
    # =====================================================

    user_posts = (
        Post.objects
        .filter(
            user=profile
        )
        .select_related(
            "category",
            "user",
        )
        .prefetch_related(
            "items__images",
            "items__size_variants",
        )
        .order_by(
            "-created_at"
        )
    )

    # =====================================================
    # APPROVED POSTS
    # =====================================================

    approved_posts = user_posts.filter(
        status="approved"
    )

    # =====================================================
    # PENDING POSTS
    # =====================================================

    pending_posts = user_posts.filter(
        status="pending"
    )

    # =====================================================
    # COUNTS
    # =====================================================

    approved_post_count = (
        approved_posts.count()
    )

    pending_post_count = (
        pending_posts.count()
    )

    post_count = (
        user_posts.count()
    )

    # =====================================================
    # WISHLIST
    # =====================================================

    wishlist_count = (
        Wishlist.objects
        .filter(
            user=request.user
        )
        .count()
    )

    # =====================================================
    # ACTIVE TAB
    # =====================================================

    active_tab = request.GET.get(
        "tab",
        "approved",
    )

    if active_tab not in [
        "approved",
        "pending",
    ]:

        active_tab = "approved"

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "profile": profile,

        "seller": request.user,

        "user_posts": user_posts,

        "approved_posts": approved_posts,

        "pending_posts": pending_posts,

        "approved_post_count":
            approved_post_count,

        "pending_post_count":
            pending_post_count,

        "post_count":
            post_count,

        "wishlist_count":
            wishlist_count,

        "is_owner": True,

        "active_tab":
            active_tab,
    }

    return render(
        request,
        "user/dashboard.html",
        context,
    )


# =========================================================
# PUBLIC SELLER PROFILE
# =========================================================
#
# VISITOR:
#   - Approved posts only
#
# OWNER:
#   - Approved posts
#   - Pending posts
#
# Same dashboard.html is used.
# =========================================================

def seller_profile(request, username):

    # =====================================================
    # GET SELLER
    # =====================================================

    seller = get_object_or_404(
        User,
        username=username,
    )

    # =====================================================
    # GET PROFILE
    # =====================================================

    profile = get_object_or_404(
        Profile,
        user=seller,
    )

    # =====================================================
    # OWNER CHECK
    # =====================================================

    is_owner = (
        request.user.is_authenticated
        and request.user.id == seller.id
    )

    # =====================================================
    # APPROVED POSTS
    #
    # Approved posts are publicly visible.
    # =====================================================

    approved_posts = (
        Post.objects
        .filter(
            user=profile,
            status="approved",
        )
        .select_related(
            "category",
            "user",
        )
        .prefetch_related(
            "items__images",
            "items__size_variants",
        )
        .order_by(
            "-created_at"
        )
    )

    # =====================================================
    # PENDING POSTS
    #
    # Only the owner can see pending posts.
    # =====================================================

    if is_owner:

        pending_posts = (
            Post.objects
            .filter(
                user=profile,
                status="pending",
            )
            .select_related(
                "category",
                "user",
            )
            .prefetch_related(
                "items__images",
                "items__size_variants",
            )
            .order_by(
                "-created_at"
            )
        )

    else:

        pending_posts = Post.objects.none()

    # =====================================================
    # COUNTS
    # =====================================================

    approved_post_count = (
        approved_posts.count()
    )

    pending_post_count = (
        pending_posts.count()
    )

    # =====================================================
    # WISHLIST
    #
    # Only the owner needs their wishlist count.
    # =====================================================

    if is_owner:

        wishlist_count = (
            Wishlist.objects
            .filter(
                user=request.user
            )
            .count()
        )

    else:

        wishlist_count = 0

    # =====================================================
    # ACTIVE TAB
    # =====================================================

    active_tab = request.GET.get(
        "tab",
        "approved",
    )

    # =====================================================
    # VISITOR MUST ALWAYS SEE APPROVED
    # =====================================================

    if not is_owner:

        active_tab = "approved"

    elif active_tab not in [
        "approved",
        "pending",
    ]:

        active_tab = "approved"

    # =====================================================
    # USER POSTS
    #
    # Owner:
    #   all posts
    #
    # Visitor:
    #   approved only
    # =====================================================

    if is_owner:

        user_posts = (
            Post.objects
            .filter(
                user=profile
            )
            .select_related(
                "category",
                "user",
            )
            .prefetch_related(
                "items__images",
                "items__size_variants",
            )
            .order_by(
                "-created_at"
            )
        )

        post_count = (
            user_posts.count()
        )

    else:

        user_posts = approved_posts

        post_count = (
            approved_post_count
        )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "profile": profile,

        "seller": seller,

        "user_posts": user_posts,

        "approved_posts": approved_posts,

        "pending_posts": pending_posts,

        "approved_post_count":
            approved_post_count,

        "pending_post_count":
            pending_post_count,

        "post_count":
            post_count,

        "wishlist_count":
            wishlist_count,

        "is_owner":
            is_owner,

        "active_tab":
            active_tab,
    }

    return render(
        request,
        "user/dashboard.html",
        context,
    )


# =========================================================
# EDIT PROFILE
# =========================================================

@login_required
@check_session_user
def edit_profile(request):

    profile = get_object_or_404(
        Profile,
        user=request.user,
    )

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully!"
            )

            return redirect(
                "user:dashboard"
            )

    # =====================================================
    # GET
    # =====================================================

    else:

        form = ProfileEditForm(
            instance=profile
        )

    return render(
        request,
        "user/edit_profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )


# =========================================================
# UPDATE PROFILE PICTURE
# =========================================================

@login_required
@check_session_user
def update_profile_pic(request):

    if request.method == "POST":

        profile = get_object_or_404(
            Profile,
            user=request.user,
        )

        form = ProfilePicForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():

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

                    old_path = (
                        profile.profile_pic.path
                    )

                    if os.path.exists(
                        old_path
                    ):

                        os.remove(
                            old_path
                        )

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
# DELETE PROFILE PICTURE
# =========================================================

@login_required
@check_session_user
def delete_profile_pic(request):

    if request.method == "POST":

        profile = get_object_or_404(
            Profile,
            user=request.user,
        )

        if profile.profile_pic:

            # =================================================
            # DELETE FILE
            # =================================================

            try:

                old_path = (
                    profile.profile_pic.path
                )

                if os.path.exists(
                    old_path
                ):

                    os.remove(
                        old_path
                    )

            except (
                ValueError,
                OSError,
            ):

                pass

            # =================================================
            # REMOVE DATABASE REFERENCE
            # =================================================

            profile.profile_pic = None

            profile.save(
                update_fields=[
                    "profile_pic"
                ]
            )

            messages.success(
                request,
                "Profile picture deleted successfully."
            )

    return redirect(
        "user:dashboard"
    )


# =========================================================
# VERIFY EMAIL
# =========================================================

def verify_email(request):

    pending = request.session.get(
        "pending_registration"
    )

    # =====================================================
    # NO PENDING REGISTRATION
    # =====================================================

    if not pending:

        messages.error(
            request,
            "Your registration session has expired. "
            "Please register again."
        )

        return redirect(
            "user:register"
        )

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        form = EmailVerificationForm(
            request.POST
        )

        if form.is_valid():

            entered_code = (
                form.cleaned_data[
                    "code"
                ]
            )

            correct_code = (
                pending.get(
                    "verification_code"
                )
            )

            # =================================================
            # CORRECT CODE
            # =================================================

            if entered_code == correct_code:

                # =============================================
                # GET OR CREATE USER
                # =============================================

                user = (
                    User.objects
                    .filter(
                        username=pending[
                            "username"
                        ]
                    )
                    .first()
                )

                if user is None:

                    user = (
                        User.objects
                        .create_user(
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
                    )

                else:

                    user.email = pending[
                        "email"
                    ]

                    user.set_password(
                        pending[
                            "password"
                        ]
                    )

                    user.save(
                        update_fields=[
                            "email",
                            "password",
                        ]
                    )

                # =============================================
                # CREATE / GET PROFILE
                # =============================================

                profile, created = (
                    Profile.objects
                    .get_or_create(
                        user=user
                    )
                )

                profile.fullName = (
                    pending[
                        "fullName"
                    ]
                )

                profile.phone_number = (
                    pending[
                        "phone_number"
                    ]
                )

                profile.gender = (
                    pending[
                        "gender"
                    ]
                )

                # =============================================
                # RESTORE PROFILE PICTURE
                # =============================================

                temp_pic_path = (
                    request.session.get(
                        "pending_profile_pic_path"
                    )
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
                # MARK EMAIL VERIFIED
                # =============================================

                profile.email_verified = True

                profile.verification_code = None

                profile.save()

                # =============================================
                # CLEAR REGISTRATION SESSION
                # =============================================

                request.session.pop(
                    "pending_registration",
                    None,
                )

                request.session.pop(
                    "pending_profile_pic_path",
                    None,
                )

                # =============================================
                # LOGIN USER
                # =============================================

                user.backend = (
                    "user.backends.EmailOrUsernameModelBackend"
                )

                login(
                    request,
                    user,
                )

                request.session[
                    "logged_in_user_id"
                ] = user.id

                # =============================================
                # SHOW TERMS
                # =============================================

                request.session[
                    "show_terms_policy"
                ] = True

                messages.success(
                    request,
                    "Email verified successfully. "
                    "Please review and accept the "
                    "TrustyShop Terms & Policies.",
                )

                return redirect(
                    "welcome"
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

    # =====================================================
    # GET
    # =====================================================

    else:

        form = EmailVerificationForm()

    return render(
        request,
        "user/verify_email.html",
        {
            "form": form,
        },
    )


# =========================================================
# TERMS & POLICY
# =========================================================

@login_required
@check_session_user
def terms_policy(request):

    profile = get_object_or_404(
        Profile,
        user=request.user,
    )

    # =====================================================
    # ALREADY ACCEPTED
    # =====================================================

    if profile.terms_accepted:

        request.session.pop(
            "show_terms_policy",
            None,
        )

        return redirect(
            "home"
        )

    # =====================================================
    # SHOW TERMS
    # =====================================================

    request.session[
        "show_terms_policy"
    ] = True

    return redirect(
        "welcome"
    )


# =========================================================
# ACCEPT TERMS & POLICY
# =========================================================

@login_required
@check_session_user
def accept_terms_policy(request):

    if request.method != "POST":

        return redirect(
            "welcome"
        )

    profile = get_object_or_404(
        Profile,
        user=request.user,
    )

    # =====================================================
    # ALREADY ACCEPTED
    # =====================================================

    if profile.terms_accepted:

        request.session.pop(
            "show_terms_policy",
            None,
        )

        return redirect(
            "home"
        )

    # =====================================================
    # ACCEPT TERMS
    # =====================================================

    profile.terms_accepted = True

    profile.terms_accepted_at = (
        timezone.now()
    )

    profile.save(
        update_fields=[
            "terms_accepted",
            "terms_accepted_at",
        ]
    )

    request.session.pop(
        "show_terms_policy",
        None,
    )

    messages.success(
        request,
        "Welcome to TrustyShop! "
        "Your account is now ready.",
    )

    return redirect(
        "home"
    )


# =========================================================
# FORGOT PASSWORD
# =========================================================

def forgot_password(request):

    if request.user.is_authenticated:
        return redirect(
            "home"
        )

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        form = ForgotPasswordForm(
            request.POST
        )

        if form.is_valid():

            email = (
                form.cleaned_data[
                    "email"
                ]
            )

            user = (
                User.objects
                .filter(
                    email__iexact=email,
                    is_active=True,
                )
                .first()
            )

            # =================================================
            # CREATE OTP
            # =================================================

            if user:

                # Remove previous unused OTPs

                (
                    PasswordResetOTP.objects
                    .filter(
                        user=user,
                        is_used=False,
                    )
                    .delete()
                )

                # =============================================
                # GENERATE OTP
                # =============================================

                otp = str(
                    random.randint(
                        100000,
                        999999,
                    )
                )

                # =============================================
                # EXPIRATION
                # =============================================

                now = timezone.now()

                expires_at = (
                    now
                    + timedelta(
                        minutes=5
                    )
                )

                # =============================================
                # SAVE OTP
                # =============================================

                PasswordResetOTP.objects.create(
                    user=user,
                    otp=otp,
                    expires_at=expires_at,
                )

                # =============================================
                # SEND EMAIL
                # =============================================

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

                request.session[
                    "password_reset_email"
                ] = user.email

            # =================================================
            # SECURITY MESSAGE
            # =================================================

            messages.success(
                request,
                "If an account exists with that email, "
                "a 6-digit OTP has been sent.",
            )

            return redirect(
                "user:verify_reset_otp"
            )

    # =====================================================
    # GET
    # =====================================================

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
        return redirect(
            "home"
        )

    # =====================================================
    # GET EMAIL FROM SESSION
    # =====================================================

    email = request.session.get(
        "password_reset_email"
    )

    if not email:

        messages.error(
            request,
            "Password reset session expired. "
            "Please request a new OTP.",
        )

        return redirect(
            "user:forgot_password"
        )

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        form = OTPVerificationForm(
            request.POST
        )

        if form.is_valid():

            submitted_email = (
                form.cleaned_data[
                    "email"
                ]
            )

            otp = form.cleaned_data[
                "otp"
            ]

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
                    "the reset request.",
                )

            else:

                # =============================================
                # FIND USER
                # =============================================

                user = (
                    User.objects
                    .filter(
                        email__iexact=email,
                        is_active=True,
                    )
                    .first()
                )

                if not user:

                    messages.error(
                        request,
                        "Account not found.",
                    )

                    return redirect(
                        "user:forgot_password"
                    )

                # =============================================
                # GET LATEST OTP
                # =============================================

                reset_otp = (
                    PasswordResetOTP.objects
                    .filter(
                        user=user,
                        is_used=False,
                    )
                    .order_by(
                        "-created_at"
                    )
                    .first()
                )

                # =============================================
                # OTP DOES NOT EXIST
                # =============================================

                if not reset_otp:

                    form.add_error(
                        "otp",
                        "OTP is invalid. "
                        "Please request a new OTP.",
                    )

                # =============================================
                # OTP EXPIRED
                # =============================================

                elif reset_otp.is_expired():

                    reset_otp.delete()

                    form.add_error(
                        "otp",
                        "OTP has expired. "
                        "Please request a new OTP.",
                    )

                # =============================================
                # WRONG OTP
                # =============================================

                elif reset_otp.otp != otp:

                    form.add_error(
                        "otp",
                        "Incorrect OTP.",
                    )

                # =============================================
                # CORRECT OTP
                # =============================================

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

    # =====================================================
    # GET
    # =====================================================

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
        return redirect(
            "home"
        )

    # =====================================================
    # CHECK OTP VERIFICATION
    # =====================================================

    if not request.session.get(
        "password_reset_verified"
    ):

        messages.error(
            request,
            "Please verify your OTP first.",
        )

        return redirect(
            "user:forgot_password"
        )

    # =====================================================
    # SESSION DATA
    # =====================================================

    user_id = request.session.get(
        "password_reset_user_id"
    )

    otp_id = request.session.get(
        "password_reset_otp_id"
    )

    if not user_id or not otp_id:

        messages.error(
            request,
            "Password reset session expired.",
        )

        return redirect(
            "user:forgot_password"
        )

    # =====================================================
    # GET USER
    # =====================================================

    try:

        user = (
            User.objects.get(
                id=user_id,
                is_active=True,
            )
        )

    except User.DoesNotExist:

        messages.error(
            request,
            "User account could not be found.",
        )

        return redirect(
            "user:forgot_password"
        )

    # =====================================================
    # GET OTP
    # =====================================================

    try:

        reset_otp = (
            PasswordResetOTP.objects.get(
                id=otp_id,
                user=user,
                is_used=False,
            )
        )

    except PasswordResetOTP.DoesNotExist:

        messages.error(
            request,
            "OTP is no longer valid.",
        )

        return redirect(
            "user:forgot_password"
        )

    # =====================================================
    # CHECK OTP EXPIRATION
    # =====================================================

    if reset_otp.is_expired():

        reset_otp.delete()

        request.session.pop(
            "password_reset_verified",
            None,
        )

        request.session.pop(
            "password_reset_user_id",
            None,
        )

        request.session.pop(
            "password_reset_otp_id",
            None,
        )

        request.session.pop(
            "password_reset_email",
            None,
        )

        messages.error(
            request,
            "OTP has expired. "
            "Please request a new OTP.",
        )

        return redirect(
            "user:forgot_password"
        )

    # =====================================================
    # GET RESET PAGE
    # =====================================================

    if request.method == "GET":

        form = ResetPasswordForm()

        return render(
            request,
            "user/reset_password.html",
            {
                "form": form,
            },
        )

    # =====================================================
    # POST RESET PASSWORD
    # =====================================================

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

    # =====================================================
    # GET NEW PASSWORD
    # =====================================================

    new_password = (
        form.cleaned_data[
            "new_password"
        ]
    )

    # =====================================================
    # SAVE PASSWORD
    # =====================================================

    user.set_password(
        new_password
    )

    user.save(
        update_fields=[
            "password"
        ]
    )

    # =====================================================
    # VERIFY PASSWORD WAS SAVED
    # =====================================================

    user.refresh_from_db()

    if not user.check_password(
        new_password
    ):

        messages.error(
            request,
            "Password could not be saved. "
            "Please try again.",
        )

        return render(
            request,
            "user/reset_password.html",
            {
                "form": form,
            },
        )

    # =====================================================
    # MARK OTP AS USED
    # =====================================================

    reset_otp.is_used = True

    reset_otp.save(
        update_fields=[
            "is_used"
        ]
    )

    # =====================================================
    # CLEAR PASSWORD RESET SESSION
    # =====================================================

    request.session.pop(
        "password_reset_verified",
        None,
    )

    request.session.pop(
        "password_reset_user_id",
        None,
    )

    request.session.pop(
        "password_reset_otp_id",
        None,
    )

    request.session.pop(
        "password_reset_email",
        None,
    )

    # =====================================================
    # DELETE OTP
    # =====================================================

    reset_otp.delete()

    # =====================================================
    # SUCCESS
    # =====================================================

    messages.success(
        request,
        "Your password has been changed successfully. "
        "You can now login with your new password.",
    )

    return redirect(
        "user:login"
    )