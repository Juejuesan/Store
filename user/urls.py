# user/urls.py

from django.urls import path
from . import views


app_name = "user"


urlpatterns = [

    # =====================================================
    # REGISTER
    # =====================================================

    path(
        "register/",
        views.register_view,
        name="register",
    ),

    # =====================================================
    # LOGIN
    # =====================================================

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    # =====================================================
    # PROFILE PICTURE
    # =====================================================

    path(
        "update-profile-pic/",
        views.update_profile_pic,
        name="update_profile_pic",
    ),

    # =====================================================
    # EMAIL VERIFICATION
    # =====================================================

    path(
        "verify-email/",
        views.verify_email,
        name="verify_email",
    ),

    # =====================================================
    # FORGOT PASSWORD
    # =====================================================

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password",
    ),

    # =====================================================
    # VERIFY PASSWORD RESET OTP
    # =====================================================

    path(
        "verify-reset-otp/",
        views.verify_reset_otp,
        name="verify_reset_otp",
    ),

    # =====================================================
    # RESET PASSWORD
    # =====================================================

    path(
        "reset-password/",
        views.reset_password,
        name="reset_password",
    ),
]