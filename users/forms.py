from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm
from django import forms
from mailings.forms import StyleFormMixin
from django.forms import ModelForm
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "avatar", "phone", "tg_name", "country",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class ManagerUpdateView(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ('email', 'is_active',)
