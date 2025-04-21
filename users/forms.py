from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obligatorio. Ingresa un email válido.")

    class Meta:
        model = User
        fields = ("username","first_name","last_name", "email", "password1", "password2")

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio", "is_private")