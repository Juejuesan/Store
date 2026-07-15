from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'phone_number', 'gender']