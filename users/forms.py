from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AdminPasswordChangeForm

User = get_user_model()





class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('email', 'phone', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Неправильный повтор пароля")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone', 'password', 'last_name', 'first_name', 'patronymic', 'birth_date',
                  'personal_data_processing', 'mailing', 'registration_by_code', 'is_superuser',
                  'is_staff', 'is_active', 'is_verified')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# class CustomUserCreationForm(UserCreationForm):
#     email = forms.CharField(label='Почта', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#     password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#
#     class Meta:
#         model = User
#         fields = ['email', 'phone', 'first_name', 'last_name', 'password1', 'password2']
#         labels = {
#             'email': 'E-mail',
#             'first_name': 'Имя',
#             'last_name': 'Фамилия',
#         }
#         widgets = {
#             'email': forms.TextInput(attrs={'class': 'form-input'}),
#             'phone': forms.TextInput(attrs={'class': 'form-input'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-input'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-input'}),
#         }
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Такой E-mail уже существует!")
#         return email
#
#     def clean_phone(self):
#         phone = self.cleaned_data['phone']
#         if User.objects.filter(phone=phone).exists():
#             raise forms.ValidationError("Такой номер телефона уже существует!")
#         return email



