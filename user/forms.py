from django import forms
from django.contrib.auth.models import User

from .models import Profile

# 1. Register Form
class RegisterForm(forms.ModelForm):
    fullName = forms.CharField(max_length=30,required=True)
    phone_number = forms.CharField(max_length=11, required=True,
             widget=forms.TextInput(attrs={
            'inputmode': 'numeric',  # Shows number keyboard on mobile
            'pattern': '[0-9]+',  # HTML5 validation
        }))
    address = forms.CharField(widget=forms.TextInput(), required=True)
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, required=True)
    profile_pic = forms.ImageField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']

        # Remove any non-digits (spaces, dashes, etc.)
        phone = ''.join(filter(str.isdigit, phone))

        if not phone:
            raise forms.ValidationError("Phone number must contain only digits.")

        if len(phone) < 11:
            raise forms.ValidationError("Phone number is not valid.")

        return phone

# 2. Login Form
class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

# 3. Profile Pic Update Form
class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']