from .models import Task
from notes.models import CustomUser
from rest_framework import serializers


class TasksSerializer(serializers.ModelSerializer):
    task_scheduler = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = [
            "id",
            "short_description",
            "task_description",
            "due_date",
            "due_time",
            "task_completed",
            "is_priority",
            "task_scheduler",
        ]
