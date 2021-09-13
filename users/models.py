from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from tasks.models import Task

class CustomUserManager(BaseUserManager):
    
    def create_superuser(self, email, username, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Staff must be true')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be true')

        return self.create_user(email=email, username=username, name=name, password=password, role='admin', **other_fields)
    
    
    def create_user(self, email, username, name, password, role, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name, role=role, **other_fields)
        user.set_password(password)
        user.save()
        return user
    


# Custom user model
class NewUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=70, unique=True)
    name = models.CharField(max_length=70)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)   
    role = models.CharField(max_length=30, default='user')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']
    
    def __str__(self):
        return self.username


class Assignments(models.Model):
    manager = models.ForeignKey(NewUser, related_name='manager', on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, related_name='user', on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, null=True, related_name='task', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("manager", "user")


    def __int__(self):
        return self.user
    