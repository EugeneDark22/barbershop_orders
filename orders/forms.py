from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Manager, Appointment, Master, Service, Branch


class ManagerRegistrationForm(UserCreationForm):
    """Форма реєстрації менеджера з вибором філії."""
    phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Введіть телефон'}))
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="Оберіть філію", required=True)

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

    discount = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        label="Знижка (%)",
        widget=forms.NumberInput(attrs={'readonly': 'readonly'})  # Робимо поле нередагованим вручну
    )

    class Meta:
        model = Appointment
        fields = ['client_name', 'phone_number', 'appointment_date', 'appointment_time', 'master', 'services', 'discount']
        widgets = {
            'client_name': forms.TextInput(attrs={'placeholder': 'Введіть ПІБ клієнта'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Введіть номер телефону'}),
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'master': forms.Select(),
        }

    def save(self, commit=True):
        """
        Перед збереженням форми перевіряємо, чи клієнт отримує знижку.
        """
        instance = super().save(commit=False)

        # Перевіряємо кількість записів клієнта та застосовуємо знижку
        previous_appointments = Appointment.objects.filter(client_name=instance.client_name).count()
        if previous_appointments >= 5:
            instance.discount = 3  # 3% знижка

        if commit:
            instance.save()
            self.save_m2m()  # Зберігаємо ManyToMany зв'язки (послуги)

        return instance


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
