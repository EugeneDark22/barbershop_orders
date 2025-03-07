from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count

class Branch(models.Model):
    """Модель для збереження філій."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва філії")

    def __str__(self):
        return self.name

class Manager(AbstractUser):
    """Оновлена модель менеджера з вибором філії."""
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Філія")

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
    services = models.ManyToManyField(Service, verbose_name="Послуги", related_name="masters")

    def __str__(self):
        return self.full_name


class Appointment(models.Model):
    client_name = models.CharField(max_length=100, verbose_name="ПІБ клієнта")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефону")
    appointment_date = models.DateField(verbose_name="Дата запису")
    appointment_time = models.TimeField(verbose_name="Час запису")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Майстер")
    services = models.ManyToManyField(Service, verbose_name="Обрані послуги")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Знижка у %")

    def save(self, *args, **kwargs):
        """
        Перед збереженням перевіряємо кількість записів клієнта.
        Якщо клієнт відвідував заклад 5 або більше разів, йому надається фіксована знижка 3%.
        """
        client_appointments = Appointment.objects.filter(client_name=self.client_name).count()

        if client_appointments >= 5:
            self.discount = 3  # Фіксована знижка 3%
        else:
            self.discount = 0  # Якщо менше 5 записів, знижка відсутня

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client_name} - {self.master.full_name} ({self.appointment_date} {self.appointment_time})"
