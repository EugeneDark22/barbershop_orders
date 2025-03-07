from django.contrib import admin
from .models import Manager, Branch

admin.site.register(Branch)

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'branch', 'is_staff', 'is_superuser')
    list_filter = ('branch', 'is_staff', 'is_superuser')
    search_fields = ('username', 'phone')
