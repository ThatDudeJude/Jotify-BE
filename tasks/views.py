from base.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from .models import Task
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .serializers import TasksSerializer
import json

# Create your views here.


class TasksList(APIView):
    def get_scheduler(self, request):
        token = Token.objects.get(user=request.user)
        if request.auth.key == token.key:
            user = CustomUser.objects.get(email=request.user.email)
            return user
        else:
            return Response(
                {"message": "Unauthorized access attempted! Please log in."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @permission_classes([permissions.IsAuthenticated])
    def get(self, request, format=None):
        scheduler = self.get_scheduler(request)
        tasks = Task.objects.filter(task_scheduler=scheduler)
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([permissions.IsAuthenticated])
    def post(self, request, format=None):
        serializer = TasksSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    def get_scheduler(self, request):
        token = Token.objects.get(user=request.user)
        if request.auth.key == token.key:
            user = CustomUser.objects.get(email=request.user.email)
            return user
        else:
            return Response(
                {"message": "Unauthorized access attempted! Please log in."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def get_task(self, pk, scheduler):
        try:
            task = Task.objects.get(pk=pk, task_scheduler=scheduler)
            return task
        except ObjectDoesNotExist:
            return Response(
                {"message": "Task does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @permission_classes([permissions.IsAuthenticated])
    def get(self, request, pk, format=None):
        scheduler = self.get_scheduler(request)
        task = self.get_task(pk, scheduler)
        serializer = TasksSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([permissions.IsAuthenticated])
    def put(self, request, pk, format=None):
        scheduler = self.get_scheduler(request)
        task = self.get_task(pk, scheduler)
        serializer = TasksSerializer(
            task, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([permissions.IsAuthenticated])
    def delete(self, request, pk, format=None):
        scheduler = self.get_scheduler(request)
        task = self.get_task(pk, scheduler)
        task.delete()
        return Response(
            {"message": "Task deleted successfully"}, status=status.HTTP_200_OK
        )
