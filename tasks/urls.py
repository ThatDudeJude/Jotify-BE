from django.urls import path
from .views import TasksList, TaskDetail

urlpatterns = [
    path("", TasksList.as_view(), name="all_tasks"),
    path("task/<int:pk>/", TaskDetail.as_view(), name="task_detail"),
]
