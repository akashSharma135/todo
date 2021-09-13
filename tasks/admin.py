from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id' ,'task_title', 'task_description', 'task_status'
    ]