from django import forms
from django.contrib.auth.models import User

from .models import Profile

# 1. Register Form
class RegisterForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=True)
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

# 2. Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

# 3. Profile Pic Update Form
class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']