from django.forms.models import ModelForm
from .models import Task


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            "task_scheduler",
            "short_description",
            "task_description",
            "due_date",
            "due_time",
            "task_completed",
            "is_priority",
        ]
