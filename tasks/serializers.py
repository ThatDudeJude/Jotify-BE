from .models import Task
from notes.models import CustomUser
from rest_framework import serializers
from .models import TASK_PRIORITY_CHOICES

class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]
    
    def to_internal_value(self, data):
        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)
        
class TasksSerializer(serializers.ModelSerializer):
    task_scheduler = serializers.HiddenField(default=serializers.CurrentUserDefault())    
    task_priority = ChoiceField(choices=TASK_PRIORITY_CHOICES)
    class Meta:
        model = Task
        fields = [
            "id",
            "short_description",
            "task_description",
            "due_date",
            "due_time",
            "task_completed",
            "task_priority",
            "task_scheduler",
        ]
