from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterModelForm(forms.ModelForm):
    re_password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 're_password']
        widgets = {
            "password": forms.PasswordInput
        }

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise ValidationError(params=password, message='Passwords don\'nt match')

        return self.cleaned_data

class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=200, widget=forms.EmailInput())
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError('User doesn\'t exists!')

        return email


