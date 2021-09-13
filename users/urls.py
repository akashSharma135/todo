from django.urls import path
from .views import AssignmentsView, UnassignManagerView, UserRegisterView, LoginView, ProfileView, AllManagersView, AllSimpleUserView, UserDetailView, AssignManagerView

urlpatterns = [
    path('auth/register', UserRegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', ProfileView.as_view()),
    path('all-managers', AllManagersView.as_view()),
    path('all-users', AllSimpleUserView.as_view()),
    path('user/<int:pk>', UserDetailView.as_view()),
    path('assign-manager', AssignManagerView.as_view()),
    path('all-assignments', AssignmentsView.as_view()),
    path('unassign-manager/<int:pk>', UnassignManagerView.as_view()),
]
