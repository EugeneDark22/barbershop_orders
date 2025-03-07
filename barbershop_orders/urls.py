from django.urls import path
from orders.views import login_user, index_page, logout_view, register_manager, appointment_view, add_master, \
    clients_list, services_list, reports_view

urlpatterns = [
    path('', login_user, name='login'),  # Головна сторінка → логін
    path('home/', index_page, name='home'),  # Головна сторінка після входу
    path('logout/', logout_view, name='logout_view'),  # Вихід
    path('register/', register_manager, name='register_manager'),  # Реєстрація
    path('appointment/', appointment_view, name='appointment'),
    path('add_master/', add_master, name='add_master'),
    path('clients/', clients_list, name='clients_list'),
    path('services/', services_list, name='services_list'),
    path('reports/', reports_view, name='reports_view'),
]
