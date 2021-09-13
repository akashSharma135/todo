from .views import AllTaskView, DeleteTaskView, TaskView
from django.urls import path
from .views import AssignTaskView, UpdateTaskStatusView

urlpatterns = [
    path('add-task', TaskView.as_view()),
    path('assign-task', AssignTaskView.as_view()),
    path('update-status', UpdateTaskStatusView.as_view()),
    path('all-tasks', AllTaskView.as_view()),
    path('delete-task/<int:pk>', DeleteTaskView.as_view())
]
