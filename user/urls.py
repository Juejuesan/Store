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

path(
    "profile/<str:username>/",
    views.seller_profile,
    name="seller-profile",
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
    # DELETE PROFILE PICTURE
    # =====================================================

    path(
        "delete-profile-pic/",
        views.delete_profile_pic,
        name="delete_profile_pic",
    ),


    # =====================================================
    # EDIT PROFILE
    # =====================================================

    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile",
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
    # TERMS & POLICY
    #
    # Shown after successful email verification.
    # =====================================================

    path(
        "terms-policy/",
        views.terms_policy,
        name="terms_policy",
    ),


    # =====================================================
    # ACCEPT TERMS & POLICY
    #
    # Called when user clicks:
    # "Agree & Continue"
    # =====================================================

    path(
        "accept-terms-policy/",
        views.accept_terms_policy,
        name="accept_terms_policy",
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

# =====================================================
# EDIT PROFILE
# =====================================================

path(
    "terms-policy/",
    views.terms_policy,
    name="terms_policy",
),

path(
    "accept-terms/",
    views.accept_terms_policy,
    name="accept_terms_policy",
),
]