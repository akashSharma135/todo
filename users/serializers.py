from rest_framework import serializers
from .models import NewUser, Assignments

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'


class AssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignments
        fields = ['id', 'manager', 'user', 'task_id']