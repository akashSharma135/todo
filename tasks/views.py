from django.db.models import manager
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from rest_framework.permissions import IsAdminUser
from users.serializers import AssignmentsSerializer
from users.models import Assignments
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import TaskSerializer

# task view
class TaskView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        task_title = request.data.get('task_title')
        task_description = request.data.get('task_description')

        task = Task.objects.create(task_title=task_title, task_description=task_description)
        task.save()

        return Response({"msg": "Task added successfully"}, status=status.HTTP_200_OK)

    
# View tasks
class AllTaskView(APIView):
    def get(self, request):
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

# Assign task
class AssignTaskView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        manager_id = request.data.get('manager_id')
        user_id = request.data.get('user_id')
        task_id = request.data.get('task_id')

        obj = Assignments.objects.filter(manager=manager_id)
        serializer = AssignmentsSerializer(obj, many=True)
        if serializer.data[0].get('user') != user_id:
            return Response({"msg": "You are not assigned to this user"})
        
        obj.update(task_id=task_id)
        
        return Response("Task Assigned!", status=status.HTTP_200_OK)

# update task status
class UpdateTaskStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
    
        task_id = request.data.get('task_id')
        status= request.data.get('status')
        if request.user.role == 'user':
            
            obj = Assignments.objects.filter(user=request.user.id)
            serializer = AssignmentsSerializer(obj, many=True)
            if not serializer:
                return Response("error")
            if serializer.data[0].get('id') != task_id:
                return Response({"msg": "You are not assigned to this task"})
            
            task_status = Task.objects.filter(id=task_id)
            task_status.update(task_status=status)
        return Response({"msg": "Task status updated!"})
        