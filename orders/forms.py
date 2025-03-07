from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Manager, Appointment, Master, Service


class ManagerRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Введіть телефон'}))
    branch = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Введіть філію'}))

    class Meta:
        model = Manager
        fields = ['username', 'phone', 'branch', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введіть логін'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Введіть пароль'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль'}),
        }

class AppointmentForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Оберіть послуги"
    )

    class Meta:
        model = Appointment
        fields = ['client_name', 'phone_number', 'appointment_date', 'appointment_time', 'master', 'services']
        widgets = {
            'client_name': forms.TextInput(attrs={'placeholder': 'Введіть ПІБ клієнта'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Введіть номер телефону'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'master': forms.Select(),
        }

class MasterForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ['full_name', 'services']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Введіть ПІБ майстра'}),
            'services': forms.CheckboxSelectMultiple(),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Назва послуги'}),
            'description': forms.Textarea(attrs={'placeholder': 'Опис послуги', 'rows': 3}),
            'price': forms.NumberInput(attrs={'placeholder': 'Ціна'}),
        }


class ReportFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата початку"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата закінчення"
    )

