from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput
from .models import Schedule
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

class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('summary', 'description', 'start_time', 'end_time')
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time

class SimpleScheduleForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""

    class Meta:
        model = Schedule
        fields = ('summary', 'date',)
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'date': forms.HiddenInput,
        }