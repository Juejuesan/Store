from django import forms
from django.contrib.auth.models import User

from .emailValidator import check_email_with_abstract
from .models import Profile


# ==========================================
# REGISTER FORM
# ==========================================

class RegisterForm(forms.ModelForm):

    fullName = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": " "
            }
        )
    )

    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "inputmode": "numeric",
                "pattern": "[0-9]{11}",
                "maxlength": "11"
            }
        )
    )

    address = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": " "
            }
        )
    )

    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                "class": "gender-select"
            }
        )
    )

    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "id": "id_profile_pic",
                "accept": "image/*"
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "id": "id_password",
                "autocomplete": "new-password"
            }
        )
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "id": "id_confirm_password",
                "autocomplete": "new-password"
            }
        )
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
                    "placeholder": " "
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": " "
                }
            ),
        }

    # ======================================
    # USERNAME
    # ======================================

    def clean_username(self):

        username = self.cleaned_data.get("username")

        if User.objects.filter(
            username__iexact=username
        ).exists():

            raise forms.ValidationError(
                "Username is already taken."
            )

        return username

    # ======================================
    # EMAIL
    # ======================================

    def clean_email(self):

        email = self.cleaned_data.get("email")

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

    # ======================================
    # PHONE
    # ======================================

    def clean_phone_number(self):

        phone = self.cleaned_data.get("phone_number")

        phone = "".join(
            filter(str.isdigit, phone)
        )

        if len(phone) != 11:

            raise forms.ValidationError(
                "Phone number must contain exactly 11 digits."
            )

        if Profile.objects.filter(
            phone_number=phone
        ).exists():

            raise forms.ValidationError(
                "This phone number is already registered."
            )

        return phone

    # ======================================
    # PASSWORD
    # ======================================

    def clean_password(self):

        password = self.cleaned_data.get("password")

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

    # ======================================
    # CONFIRM PASSWORD
    # ======================================

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

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


# ==========================================
# LOGIN FORM
# ==========================================

class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "id": "id_username",
                "autocomplete": "username"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": " ",
                "id": "id_login_password",
                "autocomplete": "current-password"
            }
        )
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )


# ==========================================
# PROFILE PICTURE
# ==========================================

class ProfilePicForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            "profile_pic"
        ]

# ==========================================
# EMAIL VERIFICATION
# ==========================================

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
                "maxlength": "6"
            }
        )
    )