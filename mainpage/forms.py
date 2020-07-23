from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# import datetime #for checking renewal date range.

class RegisterForm(forms.Form):
    firstname = forms.CharField(label='Введите имя', widget=forms.TextInput)
    surname = forms.CharField(label='Введите фамилию', widget=forms.TextInput)
    username = forms.CharField(label='Введите пользовательское имя(логин)')
    email = forms.EmailField(label='Введите адрес электронной почты')
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean_firstname(self):
        data = self.cleaned_data['firstname']

        if not data.istitle():
            raise ValidationError(_('Введите имя с заглавной буквы!'))

        if not data.isalpha():
            raise ValidationError(_('Имя должно состоять только из букв!'))

        return data

    def clean_surname(self):
        data = self.cleaned_data['surname']

        if not data.istitle():
            raise ValidationError(_('Введите фамилию с заглавной буквы!'))

        if not data.isalpha():
            raise ValidationError(_('Фамилия должна состоять только из букв!'))

        return data

    def clean_password(self):
        data1 = self.cleaned_data['password1']
        data2 = self.cleaned_data['password2']

        if data1 != data2:
            raise ValidationError(_('Пароль должен совпадать!'))

        return

class UserDeleteForm(forms.Form):
    nothing = ''

class ChangeUserProfile(forms.Form):
    firstname = forms.CharField(label='Ваше имя', widget=forms.TextInput)
    surname = forms.CharField(label='Ваша фамилия', widget=forms.TextInput)
    username = forms.CharField(label='Ваше пользовательское имя(ваш логин)')
    email = forms.EmailField(label='Ваш адрес электронной почты')

    def set_pk(self, pk):
        self.pk = pk

    def get_fields(self):
        user = User.objects.get(pk=self.pk)
        self.fields['firstname'] = forms.CharField(label='Ваше имя', widget=forms.TextInput, initial=user.first_name)
        self.fields['surname'] = forms.CharField(label='Ваша фамилия', widget=forms.TextInput, initial=user.last_name)
        self.fields['username'] = forms.CharField(label='Ваше пользовательское имя(ваш логин)', initial=user.get_username())
        self.fields['email'] = forms.EmailField(label='Ваш адрес электронной почты', initial=user.email)
        return self

    def clean_firstname(self):
        data = self.cleaned_data['firstname']

        if not data.istitle():
            raise ValidationError(_('Введите имя с заглавной буквы!'))

        if not data.isalpha():
            raise ValidationError(_('Имя должно состоять только из букв!'))

        return data

    def clean_surname(self):
        data = self.cleaned_data['surname']

        if not data.istitle():
            raise ValidationError(_('Введите фамилию с заглавной буквы!'))

        if not data.isalpha():
            raise ValidationError(_('Фамилия должна состоять только из букв!'))

        return data
