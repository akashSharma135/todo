from django.contrib import admin
from .models import NewUser, Assignments



admin.site.register(NewUser)

@admin.register(Assignments)
class ManagerAssignedAdmin(admin.ModelAdmin):
    list_display = ['id', 'manager', 'user']