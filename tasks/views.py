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
from rest_framework.parsers import JSONParser

# task view
class TaskView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

    
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
        

class DeleteTaskView(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, pk):
        try:
            task = Task.objects.filter(pk=pk)
            task.delete()
            return Response({"msg": "Task deleted!"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "No task found"}, status=status.HTTP_404_NOT_FOUND)