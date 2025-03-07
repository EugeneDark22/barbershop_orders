from django.urls import path

from django.contrib import admin
from orders.views import login_user, index_page, logout_view, register_manager, appointment_view, add_master, \
    clients_list, services_list, reports_view, delete_appointment, delete_client, delete_master, delete_service

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_user, name='login'),  # Головна сторінка → логін
    path('home/', index_page, name='home'),  # Головна сторінка після входу
    path('logout/', logout_view, name='logout_view'),  # Вихід
    path('register/', register_manager, name='register_manager'),  # Реєстрація
    path('appointment/', appointment_view, name='appointment'),
    path('add_master/', add_master, name='add_master'),
    path('clients/', clients_list, name='clients_list'),
    path('services/', services_list, name='services_list'),
    path('reports/', reports_view, name='reports_view'),
    path('delete_appointment/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('delete_client/<str:client_name>/', delete_client, name='delete_client'),
    path('delete_master/<int:master_id>/', delete_master, name='delete_master'),
    path('delete_service/<int:service_id>/', delete_service, name='delete_service'),
]
