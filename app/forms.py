from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput
"""
from django.contrib.auth.forms import AuthenticationForm
"""

#ユーザ新規登録フォーム
class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()

#ユーザログインフォーム

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput())
    
    """

class LoginForm(AuthenticationForm):
    """"""ログインフォーム""""""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  

    """