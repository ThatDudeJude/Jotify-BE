from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import json
import datetime

# Create your tests here.


class TaskTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.task_scheduler = get_user_model().objects.create_user(
            email="user@example.com", name="userexample", password="1234567890"
        )
        cls.task_scheduler.save()
        cls.task = Task(
            task_scheduler=cls.task_scheduler,
            short_description="This is a task for testing",
            task_description=" This task is just meant for testing.",
            due_date=datetime.date(2023, 4, 13).isoformat(),
            due_time=datetime.time(20, 00).isoformat(),
        )
        cls.task.save()
        cls.client.post(
            reverse("custom_login"),
            {
                "email": cls.task_scheduler.email,
                "password": "1234567890",
            },
            format="json",
        )
        cls.token = Token.objects.get(user=cls.task_scheduler).key

    def test_task_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(reverse("all_tasks"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]["id"], self.task.id)
        self.assertEqual(
            json.loads(response.content)[0]["short_description"],
            self.task.short_description,
        )
        self.assertEqual(
            json.loads(response.content)[0]["task_description"],
            self.task.task_description,
        )
        self.assertEqual(
            json.loads(response.content)[0]["due_date"], self.task.due_date
        )
        self.assertEqual(
            json.loads(response.content)[0]["due_time"], self.task.due_time
        )

    def test_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.post(
            reverse("all_tasks"),
            {
                "short_description": "Task Creation Test",
                "task_description": "Test task creation.",
                "due_date": "2023-04-14",
                "due_time": "20:30:00",
                "task_completed": False,
                "task_priority": "Low",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)["id"], 2)
        self.assertEqual(
            json.loads(response.content)["short_description"],
            "Task Creation Test",
        )
        self.assertEqual(
            json.loads(response.content)["task_description"],
            "Test task creation.",
        )
        self.assertEqual(json.loads(response.content)["due_date"], "2023-04-14")
        self.assertEqual(json.loads(response.content)["due_time"], "20:30:00")
        self.assertFalse(json.loads(response.content)["task_completed"])
        self.assertEqual(json.loads(response.content)["task_priority"], "Low")

    def test_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.put(
            reverse("task_detail", kwargs={"pk": 1}),
            {
                "short_description": "Test task update",
                "task_description": "This tests task update.",
                "due_date": "2023-04-15",
                "due_time": "21:30:00",
                "task_completed": True,
                "task_priority": "High",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse("task_detail", kwargs={"pk": 1}))
        self.assertEqual(json.loads(response.content)["id"], 1)
        self.assertEqual(
            json.loads(response.content)["short_description"],
            "Test task update",
        )
        self.assertEqual(
            json.loads(response.content)["task_description"],
            "This tests task update.",
        )
        self.assertEqual(json.loads(response.content)["due_date"], "2023-04-15")
        self.assertEqual(json.loads(response.content)["due_time"], "21:30:00")
        self.assertTrue(json.loads(response.content)["task_completed"])
        self.assertEqual(json.loads(response.content)["task_priority"], "High")
