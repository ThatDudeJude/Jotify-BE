from django.contrib import admin
from .models import Task
from .forms import CreateTaskForm

# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = CreateTaskForm
    list_display = [
        "task_scheduler",
        "short_description",
        "due_date",
    ]
    list_filter = ("task_scheduler", "task_priority")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "short_description",
                    "task_description",
                    "due_date",
                    "due_time",
                    "task_completed",
                    "task_priority",
                    "task_scheduler",
                ),
            },
        ),
    )
