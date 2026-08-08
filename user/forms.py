
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .emailValidator import check_email_with_abstract
from .models import Profile


# =========================================================
# PHONE VALIDATOR
# 09 + 6 to 9 digits
# Total length: 8 to 11 digits
# =========================================================

phone_validator = RegexValidator(
    regex=r"^09\d{6,9}$",
    message="Phone number must start with 09 and contain 8 to 11 digits.",
    code="invalid_phone",
)


# =========================================================
# REGISTER FORM
# =========================================================

class RegisterForm(forms.ModelForm):

    # -----------------------------------------------------
    # FULL NAME
    # -----------------------------------------------------

    fullName = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "autocomplete": "name",
            }
        ),
    )

    # -----------------------------------------------------
    # PHONE NUMBER
    # -----------------------------------------------------

    phone_number = forms.CharField(
        min_length=8,
        max_length=11,
        required=True,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "inputmode": "numeric",
                "autocomplete": "tel",
                "pattern": r"09\d{6,9}",
                "maxlength": "11",
            }
        ),
    )

    # -----------------------------------------------------
    # ADDRESS
    # -----------------------------------------------------

    address = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "autocomplete": "street-address",
            }
        ),
    )

    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------

    gender = forms.ChoiceField(
        choices=[
            ("", "Select your gender"),
            *Profile.GENDER_CHOICES,
        ],
        required=True,
        widget=forms.Select(
            attrs={
                "class": "gender-select",
            }
        ),
    )

    # -----------------------------------------------------
    # PROFILE PICTURE
    # -----------------------------------------------------

    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "id": "id_profile_pic",
                "accept": "image/*",
            }
        ),
    )

    # -----------------------------------------------------
    # PASSWORD
    # -----------------------------------------------------

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "id": "id_password",
                "autocomplete": "new-password",
            }
        ),
    )

    # -----------------------------------------------------
    # CONFIRM PASSWORD
    # -----------------------------------------------------

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "id": "id_confirm_password",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": " ",
                    "autocomplete": "username",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": " ",
                    "autocomplete": "email",
                }
            ),
        }

    # =====================================================
    # USERNAME VALIDATION
    # =====================================================

    def clean_username(self):

        username = self.cleaned_data.get("username")

        if not username:
            return username

        if User.objects.filter(
            username__iexact=username
        ).exists():

            raise forms.ValidationError(
                "Username is already taken."
            )

        return username

    # =====================================================
    # EMAIL VALIDATION
    # =====================================================

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if not email:
            return email

        if User.objects.filter(
            email__iexact=email
        ).exists():

            raise forms.ValidationError(
                "Email is already registered."
            )

        is_valid, message = check_email_with_abstract(email)

        if not is_valid:
            raise forms.ValidationError(message)

        return email

    # =====================================================
    # PHONE VALIDATION
    # =====================================================

    def clean_phone_number(self):

        phone = self.cleaned_data.get("phone_number")

        if not phone:
            return phone

        # Remove accidental spaces around the number.
        phone = phone.strip()

        # Only digits are allowed.
        if not phone.isdigit():

            raise forms.ValidationError(
                "Phone number must contain digits only."
            )

        # Must start with 09.
        if not phone.startswith("09"):

            raise forms.ValidationError(
                "Phone number must start with 09."
            )

        # Must contain 8 to 11 digits.
        if not 8 <= len(phone) <= 11:

            raise forms.ValidationError(
                "Phone number must contain 8 to 11 digits."
            )

        # Prevent duplicate phone numbers.
        if Profile.objects.filter(
            phone_number=phone
        ).exists():

            raise forms.ValidationError(
                "This phone number is already registered."
            )

        return phone

    # =====================================================
    # PASSWORD VALIDATION
    # =====================================================

    def clean_password(self):

        password = self.cleaned_data.get("password")

        if not password:
            return password

        if len(password) < 8:

            raise forms.ValidationError(
                "Password must be at least 8 characters."
            )

        if len(password) > 20:

            raise forms.ValidationError(
                "Password cannot exceed 20 characters."
            )

        special_chars = r'[@_!#$%^&*()<>?/\|}{~:]'

        if not any(
            char in special_chars
            for char in password
        ):

            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        return password

    # =====================================================
    # PASSWORD CONFIRMATION
    # =====================================================

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if (
            password
            and confirm_password
            and password != confirm_password
        ):

            self.add_error(
                "confirm_password",
                "Passwords do not match."
            )

        return cleaned_data


# =========================================================
# LOGIN FORM
# =========================================================

class LoginForm(forms.Form):

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "id": "id_username",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "id": "id_login_password",
                "autocomplete": "current-password",
            }
        ),
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )


# =========================================================
# PROFILE PICTURE FORM
# =========================================================

class ProfilePicForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            "profile_pic",
        ]


# =========================================================
# EMAIL VERIFICATION FORM
# =========================================================

class EmailVerificationForm(forms.Form):

    code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Enter 6-digit code",
                "inputmode": "numeric",
                "maxlength": "6",
                "autocomplete": "one-time-code",
            }
        ),
    )

    def clean_code(self):

        code = self.cleaned_data.get("code")

        if not code:
            return code

        if not code.isdigit():

            raise forms.ValidationError(
                "Verification code must contain numbers only."
            )

        if len(code) != 6:

            raise forms.ValidationError(
                "Verification code must contain exactly 6 digits."
            )

        return code