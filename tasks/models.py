from django.db import models
from notes.models import CustomUser

# Create your models here.


class Task(models.Model):
    scheduler = models.ForeignKey(
        to=CustomUser,
        related_name="scheduled_tasks",
        name="task_scheduler",
        on_delete=models.CASCADE,
    )
    short_description = models.CharField(
        blank=False, null=False, max_length=25, name="short_description"
    )
    desciption_note = models.TextField(
        blank=False, null=False, max_length=200, name="task_description"
    )
    due_date = models.DateField(blank=False, null=False, name="due_date")
    due_time = models.TimeField(blank=False, null=False, name="due_time")
    done = models.BooleanField(default=False, name="task_completed")
    is_priority = models.BooleanField(default=False, name="is_priority")

    class Meta:
        ordering = ["-due_date", "-due_time"]
