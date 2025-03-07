from datetime import datetime

from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from orders.forms import ManagerRegistrationForm, AppointmentForm, MasterForm, ServiceForm, ReportFilterForm
from orders.models import Appointment, Master, Service


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')  # Якщо вже залогінений, перенаправити на головну

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправлення на головну сторінку
        else:
            return render(request, 'login.html', {'error': 'Неправильний логін або пароль'})

    return render(request, 'login.html')

@login_required(login_url='login')
def index_page(request):
    # Отримуємо найближчі записи, відсортовані за датою та часом
    upcoming_appointments = Appointment.objects.filter(
        appointment_date__gte=datetime.today()
    ).order_by('appointment_date', 'appointment_time')[:10]  # Відображаємо лише 10 записів

    return render(request, 'index.html', {'upcoming_appointments': upcoming_appointments})


def logout_view(request):
    logout(request)
    return redirect('login')  # Після виходу перенаправлення на сторінку входу

def register_manager(request):
    if request.user.is_authenticated:
        return redirect('home')  # Якщо вже залогінений, перенаправити на головну

    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ManagerRegistrationForm()

    return render(request, 'register.html', {'form': form})

def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправлення на головну сторінку після запису
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})


def add_master(request):
    if request.method == 'POST':
        form = MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_master')  # Перенаправлення на ту ж сторінку
    else:
        form = MasterForm()

    masters = Master.objects.prefetch_related('services').all()
    return render(request, 'add_master.html', {'form': form, 'masters': masters})


def clients_list(request):
    clients = Appointment.objects.values('client_name', 'phone_number').distinct()
    return render(request, 'clients.html', {'clients': clients})

def services_list(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services_list')
    else:
        form = ServiceForm()

    services = Service.objects.all()
    return render(request, 'services.html', {'form': form, 'services': services})

def reports_view(request):
    form = ReportFilterForm(request.GET or None)
    reports_data = {}

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Отримання загальної кількості послуг
        total_services = Appointment.objects.filter(
            appointment_date__range=[start_date, end_date]
        ).count()

        # Отримання загального прибутку
        total_revenue = Service.objects.filter(
            appointment__appointment_date__range=[start_date, end_date]
        ).aggregate(total=Sum('price'))['total'] or 0

        # Найпопулярніша послуга
        popular_service = Service.objects.filter(
            appointment__appointment_date__range=[start_date, end_date]
        ).annotate(count=Count('appointment')).order_by('-count').first()

        # Формуємо результати
        reports_data = {
            "total_services": total_services,
            "total_revenue": total_revenue,
            "popular_service": popular_service.name if popular_service else "Немає даних",
        }

    return render(request, 'reports.html', {'form': form, 'reports_data': reports_data})