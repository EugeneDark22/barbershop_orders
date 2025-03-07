from django.contrib.auth.models import AbstractUser
from django.db import models

class Manager(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    branch = models.CharField(max_length=100, verbose_name="Філія")

    def __str__(self):
        return self.username

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва послуги")
    description = models.TextField(verbose_name="Опис послуги", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    def __str__(self):
        return f"{self.name} - {self.price} грн"

class Master(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="ПІБ майстра")
    services = models.ManyToManyField(Service, verbose_name="Послуги")

    def __str__(self):
        return self.full_name


class Appointment(models.Model):
    client_name = models.CharField(max_length=100, verbose_name="ПІБ клієнта")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефону")
    appointment_date = models.DateField(verbose_name="Дата запису")
    appointment_time = models.TimeField(verbose_name="Час запису")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Майстер")
    services = models.ManyToManyField(Service, verbose_name="Обрані послуги")

    def __str__(self):
        return f"{self.client_name} - {self.master.full_name} ({self.appointment_date} {self.appointment_time})"
